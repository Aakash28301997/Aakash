from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from io import TextIOWrapper
import csv
from .models import *
from django.utils import timezone


@csrf_exempt
@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_csv_data(request):
    try:
        csv_file = request.FILES.get('file')
        if not csv_file:
            return JsonResponse({'error': 'CSV file not provided'}, status=400)

        decoded_file = TextIOWrapper(csv_file.file, encoding='utf-8')
        reader = csv.DictReader(decoded_file)
        records_added = 0

        dummy_run = RunDetails.objects.order_by('-run_id').first()
        if not dummy_run:
            return JsonResponse({'error': 'No RunDetails entry available in DB. Add one before uploading.'}, status=400)

        for row in reader:
            model_name = row.get("model", "-")
            input_dim = str(row.get("CL", "-"))
            model_framework = row.get("model-framework", "onnx")
            model_source = row.get("model-source", "-")
            model_class = "LLM"  # Assuming for now

            # Create or get model
            model_obj, _ = Model.objects.get_or_create(
                model_name=model_name,
                defaults={
                    'input_dim': input_dim,
                    'model_framework': model_framework,
                    'model_class': model_class,
                    'model_source': model_source
                }
            )

            # Create PerformanceConfig
            config = PerformanceConfig.objects.create(
                bs=row.get("batchsize", "1"),
                model=model_obj,
                mos=row.get("mos", "-"),
                dma="-",
                ols=row.get("ols", "-"),
                instances=row.get("instances", "1"),
                cores=row.get("aic-num-cores", "1"),
                ppp="-",
                precision=row.get("precision", "fp32"),
                cluster_sizes="-",
                max_nsp=row.get("max_nsp", "-"),
                dfs="-",
                host_app=row.get("execute-app", "-"),
                tag=row.get("tag", "-"),
                pl=row.get("PL", "-"),
                gl=row.get("GL", "-"),
                cl=row.get("CL", "-"),
                primary_tag="imported",
                custom_op=row.get("register-custom-op", "FALSE"),
                host_freq_limit="-"
            )

            # Create PerformanceResults
            result = PerformanceResults.objects.create(
                compile_time=row.get("compile_time", "0"),
                test_time=row.get("time", "0"),
                avg_cpu_usage="0",
                board_max_power=row.get("max_board_power_watts", "0"),
                soc_avg_temp=row.get("median_soc_temparature_degree_C", "0"),
                soc_max_temp=row.get("max_soc_temparature_degree_C", "0"),
                board_avg_temp=row.get("median_board_power_watts", "0"),
                board_max_temp=row.get("max_board_power_watts", "0"),
                avg_max_err_json=None,
                qacc_metric=None,
                qacc_params=None,
                status=row.get("infer_status", "PASS"),
                priority=1,
                model_meta=None,
                model_update_date=str(timezone.now()),
                network_status="NA",
                compile_log="",
                execution_log="",
                qaic_logs="",
                optrace_link="",
                commands=row.get("execution_command", ""),
                qacc_logs="",
                pgq_logs="",
                failure_cause=row.get("failure_cause", ""),
                failure_cause_log="",
                ddr_traffic_in="0",
                ddr_traffic_out="0",
                customer=row.get("customer", "unknown"),
                tdp=row.get("tdp", "0"),
                multiplication_factor=row.get("m", "1"),
                ecc=None,
                config=config,
                run=dummy_run,
                fp32_metric=None,
                qpc_size_GB=row.get("QPC_size", "-"),
                output_metrics={}
            )

            # Store performanceresults_llm
            performanceresults_llm.objects.create(
                result=result,
                prefil_tok_sec=row.get("E2E_processed(tok/sec)", "0"),
                decode_tok_sec=row.get("E2E_generated(tok/sec)", "0"),
                ttft_ms=row.get("derated_ttft(sec)", "0"),
                tpot_avg_lat_per_tok="0",
                total_tok_sec=row.get("derated_e2e_tpt_per_card(tok/sec)", "0"),
                bs=row.get("batchsize", "1"),
                pl=row.get("PL", "-"),
                gl=row.get("GL", "-"),
                cl=row.get("CL", "-")
            )

            records_added += 1

        return JsonResponse({'message': f'{records_added} records added successfully'})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)
