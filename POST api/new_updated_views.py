
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import csv, io, json
from .models import SDKData, SW_Details, Target, RunDetails, Model, Config, ECC, Results

def parse_json(row, field):
    try:
        return json.loads(row.get(field, "{}"))
    except Exception:
        return {}

def store_sdk_info(row):
    sdk_version = row.get("sdk_version", "v0")
    branch = row.get("branch", "main")
    base_version = row.get("base_version", "0.0")
    isRel = row.get("isRel", "False").lower() == "true"
    sdk = SDKData.objects.filter(sdk_version=sdk_version, branch=branch, base_version=base_version, isRel=isRel).first()
    if not sdk:
        sdk = SDKData(sdk_version=sdk_version, branch=branch, base_version=base_version, isRel=isRel)
        sdk.save()
    return sdk

def store_sw_details(row):
    sw = SW_Details.objects.filter(
        num_nsp=row.get("num_nsp", ""),
        nsp_freq=row.get("nsp_freq", ""),
        ddr_freq=row.get("ddr_freq", ""),
        compnoc_freq=row.get("compnoc_freq", ""),
        memnoc_freq=row.get("memnoc_freq", ""),
        sysnoc_freq=row.get("sysnoc_freq", "")
    ).first()
    if not sw:
        sw = SW_Details(
            num_nsp=row.get("num_nsp", ""),
            nsp_freq=row.get("nsp_freq", ""),
            ddr_freq=row.get("ddr_freq", ""),
            compnoc_freq=row.get("compnoc_freq", ""),
            memnoc_freq=row.get("memnoc_freq", ""),
            sysnoc_freq=row.get("sysnoc_freq", "")
        )
        sw.save()
    return sw

def store_target(row):
    target = Target.objects.filter(
        target_name=row.get("target_name", ""),
        host_ip=row.get("host_ip", ""),
        os=row.get("os", ""),
        device_form_factor=row.get("device_form_factor", "")
    ).first()
    if not target:
        target = Target(
            target_name=row.get("target_name", ""),
            host_ip=row.get("host_ip", ""),
            os=row.get("os", ""),
            device_form_factor=row.get("device_form_factor", "")
        )
        target.save()
    return target

def store_model(row):
    model_name = row.get("model_name", "default_model")
    model_framework = row.get("model_framework", "default_fw")
    model = Model.objects.filter(model_name=model_name, model_framework=model_framework).first()
    if not model:
        model = Model(model_name=model_name, model_framework=model_framework)
        model.save()
    return model

def store_config(row, model):
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
        model=model
    )
    config.save()
    return config

def store_ecc(row):
    ecc = ECC(
        imem_ecc=row.get("imem_ecc", ""),
        noc_ecc=row.get("noc_ecc", ""),
        mcw_ecc=row.get("mcw_ecc", ""),
        nsp_ecc=row.get("nsp_ecc", ""),
        ddr_ecc=row.get("ddr_ecc", "")
    )
    ecc.save()
    return ecc

def store_run_details(row, sdk, sw, target):
    run = RunDetails(
        user=row.get("user", ""),
        test_type=row.get("test_type", ""),
        platform=row.get("platform", ""),
        sdk_info=sdk,
        sw_info=sw,
        target=target,
        status=row.get("status", ""),
        target_app=row.get("target_app", ""),
        mode_type=row.get("mode_type", "")
    )
    run.save()
    return run

def store_result(row, run, config, ecc):
    result = Results(
        execution_time=parse_json(row, "execution_time"),
        cpu_stats=parse_json(row, "cpu_stats"),
        device_stats=parse_json(row, "device_stats"),
        model_stats=parse_json(row, "model_stats"),
        status=row.get("result_status", ""),
        multiplication_factor=row.get("multiplication_factor", ""),
        config=config,
        ecc=ecc,
        run=run
    )
    result.save()
    return result

@csrf_exempt
def upload_csv(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

    if 'file' not in request.FILES:
        return JsonResponse({"error": "CSV file not found in request"}, status=400)

    file = request.FILES['file']
    decoded = file.read().decode('utf-8')
    io_string = io.StringIO(decoded)
    reader = csv.DictReader(io_string)

    created_count = 0
    for row in reader:
        try:
            sdk = store_sdk_info(row)
            sw = store_sw_details(row)
            target = store_target(row)
            run = store_run_details(row, sdk, sw, target)
            model = store_model(row)
            config = store_config(row, model)
            ecc = store_ecc(row)
            store_result(row, run, config, ecc)
            created_count += 1
        except Exception as e:
            return JsonResponse({"error": str(e), "row": row}, status=500)

    return JsonResponse({"message": f"Uploaded successfully. Results created: {created_count}"})
