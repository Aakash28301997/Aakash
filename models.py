from django.db import models

# Create your models here.

class SW_Details(models.Model):
    sw_info_id=models.AutoField(primary_key=True)
    num_nsp=models.CharField(max_length=10)
    nsp_freq=models.CharField(max_length=10)
    ddr_freq=models.CharField(max_length=10)
    compnoc_freq=models.CharField(max_length=10)
    memnoc_freq=models.CharField(max_length=10)
    sysnoc_freq=models.CharField(max_length=10)

class Target(models.Model):
   target_id=models.AutoField(primary_key=True)
   target_name=models.CharField(max_length=50)
   host_ip=models.CharField(max_length=50)
   host_slot=models.CharField(max_length=50)
   os=models.CharField(max_length=50)
   device_form_factor=models.CharField(max_length=50)
   tdp=models.CharField(max_length=20)
   cpu=models.CharField(max_length=20, null=True)
   memory=models.CharField(max_length=50, null=True)

class SDKData(models.Model):
   sdk_id=models.AutoField(primary_key=True)
   sdk_version=models.CharField(max_length=250)
   branch=models.CharField(max_length=20)
   base_version=models.CharField(max_length=20)
   isRelease=models.BooleanField(default=False)

class PlatformSDKInfo(models.Model):
   platform_sdk_id=models.AutoField(primary_key=True)
   platform_version=models.CharField(max_length=50)
   created_date=models.DateTimeField(auto_now_add=True)

class RunDetails(models.Model):
   run_id=models.AutoField(primary_key=True)
   user=models.CharField(max_length=50)
   test_type=models.CharField(max_length=50)
   platform=models.CharField(max_length=50)
   sdk_info=models.ForeignKey(SDKData, on_delete=models.CASCADE)
   target=models.ForeignKey(Target, on_delete=models.CASCADE)
   sw_info=models.ForeignKey(SW_Details, on_delete=models.CASCADE)
   timestamp=models.DateTimeField(auto_now_add=True)
   status=models.CharField(max_length=50)
   total_configs=models.TextField(default='', null=True)

class Model(models.Model):
    model_id=models.AutoField(primary_key=True)
    model_name=models.CharField(max_length=200)
    input_dim=models.CharField(max_length=20)
    model_framework=models.CharField(max_length=50)
    model_class=models.CharField(max_length=50)
    model_source=models.TextField()

class PerformanceConfig(models.Model):
    config_id=models.AutoField(primary_key=True)
    bs=models.CharField(max_length=10)
    model=models.ForeignKey(Model,on_delete=models.CASCADE)
    mos=models.CharField(max_length=10)
    dma=models.CharField(max_length=10)
    ols=models.CharField(max_length=20)
    instances=models.CharField(max_length=20)
    cores=models.CharField(max_length=20)
    ppp=models.CharField(max_length=20)
    precision=models.CharField(max_length=20)
    cluster_sizes=models.CharField(max_length=20)
    max_nsp=models.CharField(max_length=20)
    dfs=models.CharField(max_length=10)
    #ecc=models.CharField(max_length=10)
    host_app=models.CharField(max_length=50)
    tag=models.CharField(max_length=200)
    host_freq_limit=models.CharField(max_length=50, null=True)
    custom_op=models.CharField(max_length=10,null=True)
    primary_tag=models.CharField(max_length=200,null=True,default='-')
    pl=models.CharField(max_length=200,null=True)
    gl=models.CharField(max_length=200,null=True)
    cl=models.CharField(max_length=200,null=True)
    def __str__(self):
        #return 'Model#[model-name@%s] input_dim#%s model_framework#%s model_class#%s Batch-Size#%s MOS#%s OLS#%s Instances#%s Cores#%s Precision#%s Max-NSP#%s PPP#%s Cluster-Sizes #%s DFS#%s' % (self.model.model_name,self.model.input_dim,self.model.model_framework,self.model.model_class, self.bs,self.mos,self.ols,self.instances,self.cores,self.precision,self .max_nsp,self.ppp,self.cluster_sizes,self.dfs)
        return 'Model#[model-name@%s,model_source@%s]$input_dim#%s$model_framework#%s$model_class#%s$Host-App#%s$Batch-Size#%s$MOS#%s$OLS#%s$Instances#%s$Cores#%s$Precision#%s$Max- NSP#%s$PPP#%s$Cluster-Sizes#%s$DFS#%s' % (self.model.model_name, self.model.model_source,self.model.input_dim,self.model.model_framework,self.model.model_class, self.host_app,self. bs,self.mos,self.ols,self.instances,self.cores,self.precision,self.max_nsp,self.ppp,self.cluster_sizes,self.dfs)
        #return 'Model:%s input_dim:%s model_framework:%s model_class:%s Batch-Size:%s MOS:%s OLS:%s Instances:%s Cores:%s Precision:%s PPP:%s Cluster-Sizes:%s DFS:%s' % (self.mode l.model_name, self.model.input_dim,self.model.model_framework,self.model.model_class, self.bs,self.mos,self.ols,self.instances,self.cores,self.precision,self.ppp,self.cluster_sizes ,self.dfs)



class BuildInfo(models.Model):
    info_id=models.AutoField(primary_key=True)
    module=models.CharField(max_length=50)
    commit_id=models.CharField(max_length=100)
    run=models.ForeignKey(RunDetails, on_delete=models.CASCADE)


'''class PerformanceTest(models.Model):
   test_id=models.AutoField(primary_key=True)
   config_id=models.ForeignKey(PerformanceConfig, on_delete=models.CASCADE)
   target_id=models.ForeignKey(Build_, on_delete=models.CASCADE)
   sw_info_id=models.ForeignKey(Build_Module, on_delete=models.CASCADE)'''


class ModelMeta(models.Model):
    meta_id=models.AutoField(primary_key=True)
    model_url=models.TextField()
    model=models.ForeignKey(Model, on_delete=models.CASCADE)


class ECC(models.Model):
   ecc_id = models.AutoField(primary_key=True)
   imem_ecc = models.CharField(max_length=10)
   noc_ecc = models.CharField(max_length=10)
   mcw_ecc = models.CharField(max_length=10)
   nsp_ecc = models.CharField(max_length=10)
   ddr_ecc = models.CharField(max_length=10)


class PerformanceResults(models.Model):
   result_id=models.AutoField(primary_key=True)
   compile_time=models.CharField(max_length=50)
   test_time=models.CharField(max_length=50)
   avg_cpu_usage=models.CharField(max_length=50)
   board_max_power=models.CharField(max_length=50)
   soc_avg_temp=models.CharField(max_length=50)
   soc_max_temp=models.CharField(max_length=50)
   board_avg_temp=models.CharField(max_length=50)
   board_max_temp=models.CharField(max_length=50)
   avg_max_err_json=models.JSONField(null=True)
   qacc_metric=models.JSONField(null=True)
   qacc_params=models.JSONField(null=True)
   status=models.CharField(max_length=50)
   priority=models.IntegerField()
   model_meta=models.ForeignKey(ModelMeta, null=True, on_delete=models.SET_NULL)
   model_update_date = models.CharField(max_length=100)
   network_status = models.CharField(max_length=100)
   compile_log = models.TextField()
   execution_log = models.TextField()
   qaic_logs = models.TextField()
   optrace_link = models.TextField()
   commands = models.TextField()
   qacc_logs = models.TextField()
   pgq_logs = models.TextField()
   failure_cause = models.TextField(null=True)
   failure_cause_log = models.TextField(null=True)
   ddr_traffic_in=models.CharField(max_length=50)
   ddr_traffic_out=models.CharField(max_length=50)
   customer = models.CharField(max_length=200)
   tdp = models.IntegerField(blank=True, null=True)
   multiplication_factor = models.CharField(max_length=10)
   ecc = models.ForeignKey(ECC,null=True, on_delete=models.CASCADE)
   config=models.ForeignKey(PerformanceConfig, on_delete=models.CASCADE)
   run=models.ForeignKey(RunDetails, on_delete=models.CASCADE)
   fp32_metric = models.JSONField(null=True)
   qpc_size_GB=models.CharField(max_length=200,null=True)
   output_metrics=models.JSONField()


class auto_meta(models.Model):
   meta_id=models.AutoField(primary_key=True)
   result = models.ForeignKey(PerformanceResults,null=True, on_delete=models.CASCADE)
   qid=models.CharField(max_length=250)
   soc=models.CharField(max_length=250)
   os_grouping=models.CharField(max_length=250)

class RegressionInfo(models.Model):
   regression_id=models.AutoField(primary_key=True)
   config=models.ForeignKey(PerformanceConfig, on_delete=models.CASCADE)
   ecc = models.ForeignKey(ECC,null=True, on_delete=models.CASCADE)
   run=models.ForeignKey(RunDetails, on_delete=models.CASCADE)
   baseline=models.CharField(max_length=250,null=True)
   triage_status=models.CharField(max_length=50)
   sdk_type=models.CharField(max_length=50,null=True, default='QAIC')
   triage_job_link=models.CharField(max_length=250)
   offending_commit=models.CharField(max_length=250)
   jira_number=models.CharField(max_length=50)
   jira_desc = models.TextField()
   jira_status=models.CharField(max_length=50)
   branch=models.CharField(max_length=50, null=True)
   labels=models.CharField(max_length=50, null=True)

class RegressionInfoRootcause(models.Model):
   regression_id=models.AutoField(primary_key=True)
   config=models.ForeignKey(PerformanceConfig, on_delete=models.CASCADE)
   ecc = models.ForeignKey(ECC,null=True, on_delete=models.CASCADE)
   run=models.ForeignKey(RunDetails, on_delete=models.CASCADE)
   baseline=models.CharField(max_length=250,null=True)
   triage_status=models.CharField(max_length=50)
   sdk_type=models.CharField(max_length=50,null=True, default='QAIC')
   triage_job_link=models.CharField(max_length=250)
   offending_commit=models.CharField(max_length=250)
   jira_number=models.CharField(max_length=50)
   jira_desc = models.TextField()
   jira_status=models.CharField(max_length=50)
   branch=models.CharField(max_length=50, null=True)
   jira_root_cause=models.CharField(max_length=5000,null=True)

class PipelineMoniroring(models.Model):
   pipeline_id = models.AutoField(primary_key=True)
   sdk_info = models.ForeignKey(SDKData, on_delete=models.CASCADE)
   start_time = models.DateTimeField(null=True)
   end_time = models.DateTimeField(null=True)
   tag = models.CharField(max_length=50)
   status = models.CharField(max_length=50)
   stage_completed =  models.CharField(max_length=50)
   pipeline_log_link = models.TextField()
   test_type=models.CharField(max_length=50)
   cause_of_failure = models.TextField()

class PipelineMoniroringStages(models.Model):
   stage_id = models.AutoField(primary_key=True)
   pipeline_info = models.ForeignKey(PipelineMoniroring, on_delete=models.CASCADE)
   stage_name = models.CharField(max_length=50)
   stage_status = models.CharField(max_length=50)
   stage_start_time = models.DateTimeField(null=True)
   stage_end_time = models.DateTimeField(null=True)

class CompilerSHA(models.Model):
    compiler_sha=models.CharField(max_length=200,primary_key=True)
    aic_sdk=models.CharField(max_length=200)
    qnn_sdk=models.CharField(max_length=200)

class customerviewdata_accuracy(models.Model):
   customer_id=models.AutoField(primary_key=True)
   model=models.CharField(max_length=150)
   model_url=models.CharField(max_length=250)
   input_size=models.CharField(max_length=250)
   model_framework=models.CharField(max_length=150)
   branch=models.CharField(max_length=50)
   precision=models.CharField(max_length=50)
   customer=models.CharField(max_length=250)
   max_nsp=models.CharField(max_length=50)
   platform=models.CharField(max_length=50)
   form_factor=models.CharField(max_length=200)
   tag=models.CharField(max_length=50)
   accuracy_parameter=models.JSONField(null=True)
   curr_sdk_metric=models.JSONField(null=True)
   las_sdk_metric=models.JSONField(null=True)
   # delta_sdk_metric=models.JSONField(null=True)
   sdk_version=models.CharField(max_length=250)
   apps_version=models.CharField(max_length=150)
   platform_version=models.CharField(max_length=150)
   sdk_id=models.IntegerField()
   last_rel_sdk=models.CharField(max_length=250)
   jira_number=models.CharField(max_length=50)
   # fp32_accuracy=models.CharField(max_length=200)
   regression_delta=models.CharField(max_length=155,null=True)
   is_regressed=models.IntegerField(null=True)
   is_on_par=models.IntegerField(null=True)

class performanceresults_llm(models.Model):
   llm_result_id=models.AutoField(primary_key=True)
   result = models.ForeignKey(PerformanceResults, on_delete=models.CASCADE)
   prefil_tok_sec=models.CharField(max_length=200,null=True)
   decode_tok_sec=models.CharField(max_length=200,null=True)
   ttft_ms=models.CharField(max_length=200,null=True)
   tpot_avg_lat_per_tok=models.CharField(max_length=200,null=True)
   total_tok_sec=models.CharField(max_length=200,null=True)
   bs=models.CharField(max_length=200,null=True)
   pl=models.CharField(max_length=200,null=True)
   gl=models.CharField(max_length=200,null=True)
   cl=models.CharField(max_length=200,null=True)

class customerviewdata_llm_performance(models.Model):
   customer_id=models.AutoField(primary_key=True)
   model=models.CharField(max_length=50,default='-')
   jira_number=models.CharField(max_length=50,default='-')
   tag=models.CharField(max_length=50,default='-')
   model_url=models.CharField(max_length=250,default='-')
   host_app=models.CharField(max_length=50,default='-')
   input_size=models.CharField(max_length=50,default='-')
   model_framework=models.CharField(max_length=50,default='-')
   customer=models.CharField(max_length=250,default='-')
   batch_size=models.CharField(max_length=50,default='-')
   mos=models.CharField(max_length=50,default='-')
   ols=models.CharField(max_length=50,default='-')
   instances=models.CharField(max_length=50,default='-')
   cores=models.CharField(max_length=50,default='-')
   precision=models.CharField(max_length=50,default='-')
   max_nsp=models.CharField(max_length=50,default='-')
   dfs= models.CharField(max_length=50,default='-')
   tdp=models.CharField(max_length=50,default='-')
   branch=models.CharField(max_length=50,default='-')
   platform=models.CharField(max_length=50,default='-')
   form_factor=models.CharField(max_length=200,default='-')

   sdk_version=models.CharField(max_length=50,default='-')
   apps_version=models.CharField(max_length=50,default='-')
   platform_version=models.CharField(max_length=50,default='-')
   sdk_id=models.IntegerField()
   last_rel_sdk=models.CharField(max_length=50,default='-')

   curr_prefil_tok_sec=models.CharField(max_length=50,default='-')
   curr_decode_tok_sec=models.CharField(max_length=50,default='-')
   curr_ttft_ms=models.CharField(max_length=50,default='-')
   curr_tpot_avg_lat_per_tok=models.CharField(max_length=50,default='-')
   curr_total_tok_sec=models.CharField(max_length=50,default='-')

   prev_prefil_tok_sec=models.CharField(max_length=50,default='-')
   prev_decode_tok_sec=models.CharField(max_length=50,default='-')
   prev_ttft_ms=models.CharField(max_length=50,default='-')
   prev_tpot_avg_lat_per_tok=models.CharField(max_length=50,default='-')
   prev_total_tok_sec=models.CharField(max_length=50,default='-')

   prefil_tok_sec_delta=models.CharField(max_length=50,default='-')
   decode_tok_sec_delta=models.CharField(max_length=50,default='-')
   ttft_ms_delta=models.CharField(max_length=50,default='-')
   tpot_avg_lat_per_tok_delta=models.CharField(max_length=50,default='-')
   total_tok_sec_delta=models.CharField(max_length=50,default='-')

   bs=models.CharField(max_length=200,default='-')
   pl=models.CharField(max_length=200,default='-')
   gl=models.CharField(max_length=200,default='-')
   cl=models.CharField(max_length=200,default='-')

   qpc_size_GB=models.CharField(max_length=200,default='-')
   compile_time=models.CharField(max_length=50,default='-')
root@cdcpdtex0742938-lin:/home/qraniumtest/QDigest/QApp#
root@cdcpdtex0742938-lin:/home/qraniumtest/QDigest/QApp#
root@cdcpdtex0742938-lin:/home/qraniumtest/QDigest/QApp# nano /home/qraniumtest/QDigest/QApp/views.py
root@cdcpdtex0742938-lin:/home/qraniumtest/QDigest/QApp# nano /home/qraniumtest/QDigest/QApp/views.py
root@cdcpdtex0742938-lin:/home/qraniumtest/QDigest/QApp#
root@cdcpdtex0742938-lin:/home/qraniumtest/QDigest/QApp#
root@cdcpdtex0742938-lin:/home/qraniumtest/QDigest/QApp# nano /home/qraniumtest/QDigest/QApp/views.py
root@cdcpdtex0742938-lin:/home/qraniumtest/QDigest/QApp#
root@cdcpdtex0742938-lin:/home/qraniumtest/QDigest/QApp# nano /home/qraniumtest/QDigest/QApp/cd /home/qraniumtest/QDigest/QDigest
root@cdcpdtex0742938-lin:/home/qraniumtest/QDigest/QApp# cd /home/qraniumtest/QDigest/QApp/cd /home/qraniumtest/QDigest/QDigest
bash: cd: too many arguments
root@cdcpdtex0742938-lin:/home/qraniumtest/QDigest/QApp# ls
admin.py  apps.py  compare.py  forms.py  __init__.py  migrations  models.py  __pycache__  serializers.py  static  templates  templatetags  tests.py  urls.py  utils.py  views.py
root@cdcpdtex0742938-lin:/home/qraniumtest/QDigest/QApp#
root@cdcpdtex0742938-lin:/home/qraniumtest/QDigest/QApp#
root@cdcpdtex0742938-lin:/home/qraniumtest/QDigest/QApp# nano /home/qraniumtest/QDigest/QApp/upload_csv_to_api.py
root@cdcpdtex0742938-lin:/home/qraniumtest/QDigest/QApp# nano /home/qraniumtest/QDigest/QApp/models.py
  GNU nano 6.2                                                           /home/qraniumtest/QDigest/QApp/models.py
   mos=models.CharField(max_length=50,default='-')
   ols=models.CharField(max_length=50,default='-')
   instances=models.CharField(max_length=50,default='-')
   cores=models.CharField(max_length=50,default='-')
   precision=models.CharField(max_length=50,default='-')
   max_nsp=models.CharField(max_length=50,default='-')
   dfs= models.CharField(max_length=50,default='-')
   tdp=models.CharField(max_length=50,default='-')
   branch=models.CharField(max_length=50,default='-')
   platform=models.CharField(max_length=50,default='-')
   form_factor=models.CharField(max_length=200,default='-')

   sdk_version=models.CharField(max_length=50,default='-')
   apps_version=models.CharField(max_length=50,default='-')
   platform_version=models.CharField(max_length=50,default='-')
   sdk_id=models.IntegerField()
   last_rel_sdk=models.CharField(max_length=50,default='-')

   curr_prefil_tok_sec=models.CharField(max_length=50,default='-')
   curr_decode_tok_sec=models.CharField(max_length=50,default='-')
   curr_ttft_ms=models.CharField(max_length=50,default='-')
   curr_tpot_avg_lat_per_tok=models.CharField(max_length=50,default='-')
   curr_total_tok_sec=models.CharField(max_length=50,default='-')

   prev_prefil_tok_sec=models.CharField(max_length=50,default='-')
   prev_decode_tok_sec=models.CharField(max_length=50,default='-')
   prev_ttft_ms=models.CharField(max_length=50,default='-')
   prev_tpot_avg_lat_per_tok=models.CharField(max_length=50,default='-')
   prev_total_tok_sec=models.CharField(max_length=50,default='-')

   prefil_tok_sec_delta=models.CharField(max_length=50,default='-')
   decode_tok_sec_delta=models.CharField(max_length=50,default='-')
   ttft_ms_delta=models.CharField(max_length=50,default='-')
   tpot_avg_lat_per_tok_delta=models.CharField(max_length=50,default='-')
   total_tok_sec_delta=models.CharField(max_length=50,default='-')

   bs=models.CharField(max_length=200,default='-')
   pl=models.CharField(max_length=200,default='-')
   gl=models.CharField(max_length=200,default='-')
   cl=models.CharField(max_length=200,default='-')

   qpc_size_GB=models.CharField(max_length=200,default='-')
   compile_time=models.CharField(max_length=50,default='-')

