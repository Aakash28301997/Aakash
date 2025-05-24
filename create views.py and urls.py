My Colleague delegated a work to me, said that he wanted me to use django and create a POST api which can read/import a csv file and store the data into the database. He also said that he has already 
created models.py and wants me to create views.py and urls.py,,,.. Qdata was like the project title since it had data that he had been working on currently he duplicated it and made QDigest so i can use 
that as reference. if i want to access it i have to use     /home/qraniumtest/QDigest/QApp... and if i use ican see these files such as,
admin.py  apps.py  compare.py  forms.py  __init__.py  migrations  models.py  __pycache__  serializers.py  static  templates  templatetags  tests.py  urls.py  utils.py  views.py

I have opened and saw views.py it has about 5000 lines of code which i said to my colleague he sent this messages in teams chat i send the full chat below, 

bro just saw views.py it already has 5053 line of codes
--
only refer StorePerformanceResults function,which will be used to store the data.
 
This is how we use the API POST call
 
curl -s -X POST -H 'Content-Type: application/json' -d @/prj/aicperf/new_pipeline_test/AIC.1.19.3.27/Cloud/2472/execution/Gigabyte_14NSP/results.json http://aicperf.qualcomm.com:80/app/storePerformanceResults/ --insecure
  
only refer StorePerformanceResults function
This is to store a json file but the new API should be able to store CSV file
-- 


csv file name: vllm_fix_pl_gl_mini_75.csv

	model	PL	GL	CL	batchsize	MQTS	CPL	mode_type	precision	hf-source	status	E2E_processed(tok/sec)	E2E_generated(tok/sec)	row	compile-only	time-passes	vvv	aic-perf-warnings	version-extended	aic-hw-version	aic-hw	retained-state	mxfp6-matmul	allow-mxint8-mdp-io	m	tokenizer_path	network-specialization-config	custom-IO-list-file	model-source	compile-app	execute-app	customer	model-framework	threads-per-queue	tag	compile_timeout	execute_timeout	server_timeout	e2e_lat_timeout	mos	ols	convert-to-fp16	aic-enable-depth-first	register-custom-op	beam_width	ignore-eos	derated_ttft(sec)	derated_decode_tpt_per_card(tok/sec)	derated_e2e_tpt_per_card(tok/sec)	aic-num-cores	aic-binary-dir	mdp-load-partition-config	device-id	compilation-log-path	execution-log-path	crash-dump-path	qdss-log-path	skip_keys	failure_cause	compilation_command	quantization	temperature	kv-cache-dtype	backend	trust-remote-code	seed	device	execution_command	instances	max_dram_total_KB	median_dram_total_KB	max_dram_free_KB	median_dram_free_KB	max_dram_utilization_%	median_dram_utilization_%	max_dram_bw_KBps	median_dram_bw_KBps	max_soc_power_watts	median_soc_power_watts	max_board_power_watts	median_board_power_watts	max_soc_temparature_degree_C	median_soc_temparature_degree_C	QPC_size	time	Average_TTFT(sec)	model_load_time(sec)	compile_time	infer_status
0	Llama3.1-8B	128	128	256	1	4	128	P2P	mx6	meta-llama/Llama-3.1-8B-Instruct	PASS	100.26	50.13	18	TRUE	TRUE	TRUE	TRUE	TRUE	2	TRUE	TRUE	TRUE	TRUE	/home/qraniumtest/QEFF_MODELS/qeff_cache/meta-llama/Meta-Llama-3.1-8B-Instruct/onnx_meta_llama_Meta_Llama_3.1_8B_Instruct_with_fbs/meta-llama_Meta-Llama-3.1-8B-Instruct_kv.onnx	meta-llama/Llama-3.1-8B-Instruct	/home/qraniumtest/AIC.1.20.0.100/Cloud_LLM_performance/2574/network-specialization-config/Llama3.1-8B/1_128_256.json	/home/qraniumtest/QEFF_MODELS/qeff_cache/meta-llama/Meta-Llama-3.1-8B-Instruct/onnx_meta_llama_Meta_Llama_3.1_8B_Instruct_with_fbs/custom_io_int8.yaml		/opt/qti-aic/exec/qaic-exec	/home/qraniumtest/AIC.1.20.0.100/Cloud_LLM_performance/2574/qserve/qserve/benchmarks/benchmark_throughput.py	AWS	onnx	4	cloud,LLM-KV-cache,1QPC,qnn_release	604800	604800	1800	604800			TRUE	TRUE			TRUE				16	/home/qraniumtest/AIC.1.20.0.100/Cloud_LLM_performance/2574/Binaries/Llama3.1-8B/mx6/P2P/4/bs_1_cpl_128_cl_256	/home/qraniumtest/AIC.1.20.0.100/Cloud_LLM_performance/2574/MDP-parition-file/p2p-mq-config-4.json	['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']	/home/qraniumtest/AIC.1.20.0.100/Cloud_LLM_performance/2574/Logs/Llama3.1-8B/mx6/P2P/4/bs_1_cpl_128_cl_256/compilation_log.txt	/home/qraniumtest/AIC.1.20.0.100/Cloud_LLM_performance/2574/Logs/Llama3.1-8B/mx6/P2P/4/bs_1_cpl_128_cl_256/prompt_len_128	/home/qraniumtest/AIC.1.20.0.100/Cloud_LLM_performance/2574/Qaic_crashdump/Llama3.1-8B/mx6/P2P/4/bs_1_cpl_128_cl_256/prompt_len_128	/home/qraniumtest/AIC.1.20.0.100/Cloud_LLM_performance/2574/QDSS_logs/Llama3.1-8B/mx6/P2P/4/bs_1_cpl_128_cl_256/prompt_len_128	[]		/opt/qti-aic/exec/qaic-exec -aic-binary-dir=/home/qraniumtest/AIC.1.20.0.100/Cloud_LLM_performance/2574/Binaries/Llama3.1-8B/mx6/P2P/4/bs_1_cpl_128_cl_256 -custom-IO-list-file=/home/qraniumtest/QEFF_MODELS/qeff_cache/meta-llama/Meta-Llama-3.1-8B-Instruct/onnx_meta_llama_Meta_Llama_3.1_8B_Instruct_with_fbs/custom_io_int8.yaml -m=/home/qraniumtest/QEFF_MODELS/qeff_cache/meta-llama/Meta-Llama-3.1-8B-Instruct/onnx_meta_llama_Meta_Llama_3.1_8B_Instruct_with_fbs/meta-llama_Meta-Llama-3.1-8B-Instruct_kv.onnx -allow-mxint8-mdp-io -time-passes -convert-to-fp16 -aic-hw -compile-only -aic-hw-version=2.0 -aic-perf-warnings -retained-state -version-extended -vvv -aic-num-cores=16 -network-specialization-config=/home/qraniumtest/AIC.1.20.0.100/Cloud_LLM_performance/2574/network-specialization-config/Llama3.1-8B/1_128_256.json -mxfp6-matmul -mdp-load-partition-config=/home/qraniumtest/AIC.1.20.0.100/Cloud_LLM_performance/2574/MDP-parition-file/p2p-mq-config-4.json -aic-enable-depth-first	mxfp6	0	mxint8	vllm	TRUE	20	qaic	python3 /home/qraniumtest/AIC.1.20.0.100/Cloud_LLM_performance/2574/qserve/qserve/benchmarks/benchmark_throughput.py --kv-cache-dtype mxint8 --max-seq-len-to-capture 128 --fixed-gen-len 128 --temperature 0.0 --trust-remote-code --model meta-llama/Llama-3.1-8B-Instruct --backend vllm --device qaic --num-prompts 1 --max-num-seqs 1 --max-model-len 256 --quantization mxfp6 --fixed-input-len 128 --seed 20	1	33488896	33488896	33235535	33235535	12.37	0.76	22654912	155184	15	10	49	45	44	41.5	13.38	0:00:58	0.06	12	 00:14:38	TRUE


StorePerformanceResults function from views.py

from django.shortcuts import render
from .models import *
from .forms import *
from rest_framework.decorators import api_view
import sys
from datetime import datetime
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.utils import timezone
from .serializers import *
from .utils import *
from .compare import *
import collections
from django.db.models import Sum,Max,Count,FloatField,Min
from django.db.models.functions import Cast
from django.db import connection
from collections import namedtuple
import operator
from functools import reduce
from django.db.models import Q
import json
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.timezone import make_aware
import functools
# import pandas as pd
import os
import ast
import traceback


@api_view(['GET','POST'])
def storePerformanceResults(request):
    try:
        print('store performance results',request)
        newRun = request.GET.get('newRun')
        jsonData=request.data
        print('jsonData.....',jsonData)
        user=jsonData['user']
        print('user....',user)
        test_type=jsonData['test_type']
        ''' get target details and store it to DB if not present'''
        target=jsonData["target"]
        target_name=target.get("target_name","-")
        host_ip=target.get("host_ip","-")
        host_slot=target.get("host_slot","-")
        os=target.get("os","-")
        device_form_factor=target.get("device_form_factor","-")
        tdp=target.get("tdp","-")
        cpu=target.get("cpu","-")
        memory=target.get("memory","-")
        target=Target.objects.filter(target_name=target_name,host_ip=host_ip,host_slot=host_slot,os=os,device_form_factor=device_form_factor,tdp=tdp,cpu=cpu,>
        print('target....',target.count())
        if (target.count()==0):
           target=Target(target_name=target_name,host_ip=host_ip,host_slot=host_slot,os=os,device_form_factor=device_form_factor,tdp=tdp,cpu=cpu,memory=memor>
           target.save()
           target=Target.objects.filter(target_name=target_name,host_ip=host_ip,host_slot=host_slot,os=os,device_form_factor=device_form_factor,tdp=tdp,cpu=c>

        ''' get the sdk info and store it to the DB '''
        sdk_info=storeSDKInfo(jsonData)
        ''' get sw info and persist it'''
        sw_info=persistSWDetails(jsonData)
        print('sw_info',sw_info)
        ''' persist test run info '''
        if (newRun == 'false'):
            platform = jsonData["platform"]
            testrun = TestRun.objects.filter(user=user, platform=platform, sdk_info=sdk_info[0], sw_info=sw_info[0]).order_by('-run_id')
        else:
            testrun=persistTestRunInfo(jsonData,target[0],sw_info[0],sdk_info[0])
        #testrun=persistTestRunInfo(jsonData,target[0],sw_info[0],sdk_info[0])
        print('testrun',testrun)
        ''' populate module commit-ids if test is user triggered '''
        #if (user!='system'):
           #populateModuleCommits(jsonData,testrun[0])
        print("length::::::",len(jsonData['results']))
        for key in range(len(jsonData['results'])):
            ''' get performance config and persist it to DB'''
            print(jsonData["results"][key]["config"])
            tags=jsonData["results"][key]["config"]["tag"]
            tags_list=tags.split(',')
            primary_key_list=['auto','cloud','mlperf','edge']
            primary_tag=next((item for item in primary_key_list if item in tags_list), '-')
            for tag in tags_list:
                print(tag)
                config=persistPerformanceConfig(jsonData,key,tag,primary_tag)
                ''' store performance result for the config '''
                storePerformanceResult(jsonData,key,config[0],testrun[0])
                print("ok")
        message='result stored'
    except:
        print('ERRRRRRR==>', sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
        sys.exc_info()[2]
        exception_type, exception_object, exception_traceback = sys.exc_info()
        line_number = exception_traceback.tb_lineno
        filename = exception_traceback.tb_frame.f_code.co_filename
        if 'sdk_info' in jsonData:
           sdk_info_version = jsonData['sdk_info']['sdk_version']
        else:
           sdk_info_version = 'SDK Info Missing'
        try:
           email_message = "Subject: AIC." + sdk_info_version + " " + jsonData['platform'] + "\n\n Hi Team, \n Error in result storage API line number:" + st>
           email_send_function(email_message)
        except:
           pass
        message='error in result storage...',sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]
        return JsonResponse({'message': str(message), 'error': True})
    return HttpResponse(message)




