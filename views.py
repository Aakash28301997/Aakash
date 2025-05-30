
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import csv, io, json
from .models import SDKData, SW_Details, Target, RunDetails, Model, Config, ECC, Results, PerformanceMetrics

def get_or_create_sdk(row):
    sdk_obj, _ = SDKData.objects.get_or_create(
        sdk_version=row.get("sdk_version", ""),
        branch=row.get("branch", ""),
        base_version=row.get("base_version", ""),
        defaults={"isRel": row.get("isRel", "False").lower() == "true"}
    )
    return sdk_obj

def get_or_create_sw_details(row):
    sw_obj, _ = SW_Details.objects.get_or_create(
        num_nsp=row.get("num_nsp", ""),
        nsp_freq=row.get("nsp_freq", ""),
        defaults={
            "ddr_freq": row.get("ddr_freq", ""),
            "compnoc_freq": row.get("compnoc_freq", ""),
            "memnoc_freq": row.get("memnoc_freq", ""),
            "sysnoc_freq": row.get("sysnoc_freq", "")
        }
    )
    return sw_obj

def get_or_create_target(row):
    target_obj, _ = Target.objects.get_or_create(
        target_name=row.get("target_name", ""),
        host_ip=row.get("host_ip", ""),
        os=row.get("system_os", ""),
        device_form_factor=row.get("device_form_factor", "")
    )
    return target_obj

def create_ecc(row):
    return ECC.objects.create(
        imem_ecc=row.get("imem_ecc", ""),
        moc_ecc=row.get("moc_ecc", ""),
        mcw_ecc=row.get("mcw_ecc", ""),
        nsp_ecc=row.get("nsp_ecc", ""),
        ddr_ecc=row.get("ddr_ecc", "")
    )

def get_or_create_model(row):
    model_obj, _ = Model.objects.get_or_create(
        model_name=row.get("model", "default_model"),
        model_framework=row.get("model_framework", ""),
        defaults={"vllm_dataset": row.get("vllm_dataset", "")}
    )
    return model_obj

def create_config(row, model_obj):
    return Config.objects.create(
        bs=row.get("bs", ""),
        pl=row.get("pl", ""),
        gl=row.get("gl", ""),
        cl=row.get("cl", ""),
        cpl=row.get("cpl", ""),
        mqts=row.get("mqts", ""),
        mos=row.get("mos", ""),
        dma=row.get("dma", ""),
        ols=row.get("ols", ""),
        instances=row.get("instances", ""),
        cores=row.get("cores", ""),
        ppp=row.get("ppp", ""),
        precision=row.get("precision", ""),
        cluster_sizes=row.get("cluster_sizes", ""),
        dfs=row.get("dfs", ""),
        custom_op=row.get("custom_op", ""),
        kv_precision=row.get("kv_precision", ""),
        model_id=model_obj
    )

def create_run(row, sdk_obj, sw_obj, target_obj):
    return RunDetails.objects.create(
        user=row.get("user", ""),
        test_type=row.get("test_type", ""),
        platform=row.get("platform", ""),
        status=row.get("status", ""),
        sdk_info=sdk_obj,
        sw_info=sw_obj,
        target=target_obj,
        target_app=row.get("target_app", ""),
        mode_type=row.get("tools", "")
    )

def build_results_payload(row):
    execution_time = {
        "compile_time": row.get("compile_time"),
        "execution_time": row.get("execution_time")
    }

    device_stats = {
        "median_dram_utilization_%": row.get("median_dram_utilization_%"),
        "median_dram_bw_KBps": row.get("median_dram_bw_KBps"),
        "model_load_time(sec)": row.get("model_load_time(sec)")
    }

    model_stats = {
        "qpc_size_GB": row.get("qpc_size_GB")
    }

    performance_metrics_keys = [
        "e2e_processed_tok_sec", "e2e_generated_tok_sec", "average_ttft(sec)",
        "output_token_throughput(tok/s)", "mean_ttft_sec", 
        "request_throughput(req/s)", "total_token_throughput_tok_sec"
    ]
    performance_metrics = {
        key: row.get(key) for key in performance_metrics_keys if row.get(key) is not None
    }

    return execution_time, device_stats, model_stats, performance_metrics

@csrf_exempt
def upload_csv(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

    uploaded_file = request.FILES.get("file")
    if not uploaded_file:
        return JsonResponse({"error": "CSV file not found in request"}, status=400)

    try:
        decoded = uploaded_file.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(decoded))
    except Exception as e:
        return JsonResponse({"error": f"Failed to parse CSV file: {str(e)}"}, status=400)

    created_count = 0

    for row in reader:
        try:
            sdk_obj = get_or_create_sdk(row)
            sw_obj = get_or_create_sw_details(row)
            target_obj = get_or_create_target(row)
            ecc = create_ecc(row)
            model_obj = get_or_create_model(row)
            config = create_config(row, model_obj)
            run = create_run(row, sdk_obj, sw_obj, target_obj)
            execution_time, device_stats, model_stats, performance_metrics = build_results_payload(row)

            result = Results.objects.create(
                execution_time=json.dumps(execution_time),
                cpu_stats="NA",
                device_stats=json.dumps(device_stats),
                model_stats=json.dumps(model_stats),
                multiplication_factor=row.get("multiplication_factor", ""),
                run_id=run,
                config_id=config,
                ecc_id=ecc
            )

            for key, value in performance_metrics.items():
                PerformanceMetrics.objects.create(results=result, key=key, value=value)

            created_count += 1

        except Exception as e:
            return JsonResponse({"error": str(e), "row": row}, status=500)

    return JsonResponse({"message": f"Upload successful. Rows created: {created_count}"})
