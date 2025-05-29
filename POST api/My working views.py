from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import csv, io, json
from .models import SDKData, SW_Details, Target, RunDetails, Model, Config, ECC, Results

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

    def parse_json(field, row):
        try:
            return json.loads(row.get(field, "{}"))
        except Exception:
            return {}

    for row in reader:
        try:
            # SDKData
            sdk_qs = SDKData.objects.filter(
                sdk_version=row.get("sdk_version", "v0"),
                branch=row.get("branch", "main"),
                base_version=row.get("base_version", "0.0")
            )
            if sdk_qs.exists():
                sdk_obj = sdk_qs.first()
            else:
                sdk_obj = SDKData(
                    sdk_version=row.get("sdk_version", "v0"),
                    branch=row.get("branch", "main"),
                    base_version=row.get("base_version", "0.0"),
                    isRel=row.get("isRel", "False").lower() == "true"
                )
                sdk_obj.save()

            # RunDetails
            run = RunDetails(
                user=row.get("user", ""),
                test_type=row.get("test_type", ""),
                platform=row.get("platform", ""),
                status=row.get("status", ""),
                sdk_info_id=sdk_obj,
                target_app=row.get("target_app", ""),
                mode_type=row.get("mode_type", "")
            )
            run.save()

            # SW_Details
            sw_qs = SW_Details.objects.filter(
                num_nsp=row.get("num_nsp", ""),
                nsp_freq=row.get("nsp_freq", "")
            )
            if sw_qs.exists():
                sw_obj = sw_qs.first()
            else:
                sw_obj = SW_Details(
                    num_nsp=row.get("num_nsp", ""),
                    nsp_freq=row.get("nsp_freq", ""),
                    ddr_freq=row.get("ddr_freq", ""),
                    compnoc_freq=row.get("compnoc_freq", ""),
                    memnoc_freq=row.get("memnoc_freq", ""),
                    sysnoc_freq=row.get("sysnoc_freq", "")
                )
                sw_obj.save()

            # Target
            target_qs = Target.objects.filter(
                target_name=row.get("target_name", ""),
                host_ip=row.get("host_ip", ""),
                os=row.get("os", ""),
                device_form_factor=row.get("device_form_factor", "")
            )
            if target_qs.exists():
                target_obj = target_qs.first()
            else:
                target_obj = Target(
                    target_name=row.get("target_name", ""),
                    host_ip=row.get("host_ip", ""),
                    os=row.get("os", ""),
                    device_form_factor=row.get("device_form_factor", "")
             )
                target_obj.save()

            # ECC
            ecc = ECC(
                imem_ecc=row.get("imem_ecc", ""),
                moc_ecc=row.get("moc_ecc", ""),
                mcw_ecc=row.get("mcw_ecc", ""),
                nsp_ecc=row.get("nsp_ecc", ""),
                ddr_ecc=row.get("ddr_ecc", "")
            )
            ecc.save()

            # Model
            model_qs = Model.objects.filter(
                model_name=row.get("model_name", "default_model"),
                model_framework=row.get("model_framework", "default_fw")
            )
            if model_qs.exists():
                model_obj = model_qs.first()
            else:
                model_obj = Model(
                    model_name=row.get("model_name", "default_model"),
                    model_framework=row.get("model_framework", "default_fw")
                )
                model_obj.save()

            # Config
            config = Config(
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
            config.save()

            # Results 
            result = Results(
                execution_time=row.get("execution_time", ""),
                cpu_stats=row.get("cpu_stats", "{}"),
                device_stats=row.get("device_stats", "{}"),
                model_stats=row.get("model_stats", "{}"),
                multiplication_factor=row.get("multiplication_factor", ""),
                run_id=run,
                config_id=config,
                ecc_id=ecc
            )
            result.save()
            created_count += 1

        except Exception as e:
            return JsonResponse({"error": str(e), "row": row}, status=500)

    return JsonResponse({"message": f"Upload successful. Rows created: {created_count}"})
