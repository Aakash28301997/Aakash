/Application/views.py


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import csv, io, json
import requests

from .models import SDKData, SW_Details, Target, RunDetails, Model, Config, ECC, Results

# Create your views here.
@csrf_exempt
def upload_csv(request):
    if request.method == "POST":
        if 'file' not in request.FILES:
            return JsonResponse({"error": "CSV file not found in request"}, status=400)

        file = request.FILES['file']
        decoded = file.read().decode('utf-8')
        io_string = io.StringIO(decoded)
        reader = csv.DictReader(io_string)

        created_count = 0
        for row in reader:
            try:
                model_obj, _ = Model.objects.get_or_create(
                    model_name = row.get("model_name", "default_model"),
                    model_framework = row.get("model_framework", "default_fw")
                )

                config = Config.objects.create(
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

                ecc = ECC.objects.create(
                    imem_ecc=row.get("imem_ecc", ""),
                    moc_ecc=row.get("moc_ecc", ""),
                    mcw_ecc=row.get("mcw_ecc", ""),
                    nsp_ecc=row.get("nsp_ecc", ""),
                    ddr_ecc=row.get("ddr_ecc", "")
                )

                sdk_obj, _ = SDKData.objects.get_or_create(
                    sdk_version=row.get("sdk_version", "v0"),
                    branch=row.get("branch", "main"),
                    base_version=row.get("base_version", "0.0"),
                    isRel=row.get("isRel", "False") == "True"
                )

                sw_obj, _ = SW_Details.objects.get_or_create(
                    num_nsp=row.get("num_nsp", ""),
                    nsp_freq=row.get("nsp_freq", ""),
                    ddr_freq=row.get("ddr_freq", ""),
                    compnoc_freq=row.get("compnoc_freq", ""),
                    memnoc_freq=row.get("memnoc_freq", ""),
                    sysnoc_freq=row.get("sysnoc_freq", "")
                )

                target_obj, _ = Target.objects.get_or_create(
                    target_name=row.get("target_name", ""),
                    host_ip=row.get("host_ip", ""),
                    os=row.get("os", ""),
                    device_form_factor=row.get("device_form_factor", "")
                )

                run = RunDetails.objects.create(
                    user=row.get("user", ""),
                    test_type=row.get("test_type", ""),
                    platform=row.get("platform", ""),
                    status=row.get("status", ""),
                    sdk_info_id=sdk_obj,
                    sw_info_id=sw_obj,
                    target_id=target_obj,
                    target_app=row.get("target_app", ""),
                    mode_type=row.get("mode_type", ""),
                )

                Results.objects.create(
                    execution_time=row.get("execution_time", ""),
                    cpu_stats=row.get("cpu_stats", "{}"),
                    device_stats=row.get("device_stats", "{}"),
                    model_stats=row.get("model_stats", "{}"),
                    multiplication_factor=row.get("multiplication_factor", ""),
                    config_id=config,
                    ecc_id=ecc,
                    run_id=run
                )

            except Exception as e:
                return JsonResponse({"error": str(e), "row": row}, status=500)

        return JsonResponse({"message": "Uploaded successfully."})

    return JsonResponse({"error": "Only POST method is allowed."}, status =405)

