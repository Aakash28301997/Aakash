
from django.db import models

class SDKData(models.Model):
   sdk_id = models.AutoField(primary_key=True)
   sdk_version = models.CharField(max_length=250)
   branch = models.CharField(max_length=20)
   base_version = models.CharField(max_length=20)
   isRel = models.BooleanField(default=False)

class SW_Details(models.Model):
   sw_info_id = models.AutoField(primary_key=True)
   num_nsp = models.CharField(max_length=10)
   nsp_freq = models.CharField(max_length=10)
   ddr_freq = models.CharField(max_length=10)
   compnoc_freq = models.CharField(max_length=10)
   memnoc_freq = models.CharField(max_length=10)
   sysnoc_freq = models.CharField(max_length=10)

class Target(models.Model):
   target_id = models.AutoField(primary_key=True)
   target_name = models.CharField(max_length=50)
   host_ip = models.CharField(max_length=50)
   os = models.CharField(max_length=50)
   device_form_factor = models.CharField(max_length=50)

class RunDetails(models.Model):
   run_id = models.AutoField(primary_key=True)
   user = models.CharField(max_length=50)
   test_type = models.CharField(max_length=50)
   platform = models.CharField(max_length=50)
   sdk_info = models.ForeignKey(SDKData, on_delete=models.CASCADE)
   target = models.ForeignKey(Target, on_delete=models.CASCADE)
   sw_info = models.ForeignKey(SW_Details, on_delete=models.CASCADE)
   timestamp = models.DateTimeField(auto_now_add=True)
   status = models.CharField(max_length=50)
   target_app = models.CharField(max_length=50)
   mode_type = models.CharField(max_length=50)

class Model(models.Model):
   model_id = models.AutoField(primary_key=True)
   model_name = models.CharField(max_length=200)
   model_framework = models.CharField(max_length=50)

class Config(models.Model):
   config_id = models.AutoField(primary_key=True)
   bs = models.CharField(max_length=10)
   pl = models.CharField(max_length=20, null=True)
   gl = models.CharField(max_length=20, null=True)
   cl = models.CharField(max_length=20, null=True)
   cpl = models.CharField(max_length=20, null=True)
   mqts = models.CharField(max_length=20, null=True)
   model = models.ForeignKey(Model, on_delete=models.CASCADE)
   mos = models.CharField(max_length=10)
   dma = models.CharField(max_length=10)
   ols = models.CharField(max_length=20)
   instances = models.CharField(max_length=20)
   cores = models.CharField(max_length=20)
   ppp = models.CharField(max_length=20)
   precision = models.CharField(max_length=20)
   cluster_sizes = models.CharField(max_length=20)
   dfs = models.CharField(max_length=10)
   custom_op = models.CharField(max_length=10, null=True)
   kv_precision = models.CharField(max_length=20, null=True)

class ECC(models.Model):
   ecc_id = models.AutoField(primary_key=True)
   imem_ecc = models.CharField(max_length=10)
   noc_ecc = models.CharField(max_length=10)
   mcw_ecc = models.CharField(max_length=10)
   nsp_ecc = models.CharField(max_length=10)
   ddr_ecc = models.CharField(max_length=10)

class Results(models.Model):
   result_id = models.AutoField(primary_key=True)
   execution_time = models.JSONField(null=True)
   cpu_stats = models.JSONField(null=True)
   device_stats = models.JSONField(null=True)
   model_stats = models.JSONField(null=True)
   status = models.CharField(max_length=50)
   multiplication_factor = models.CharField(max_length=10)
   ecc = models.ForeignKey(ECC, null=True, on_delete=models.CASCADE)
   config = models.ForeignKey(Config, on_delete=models.CASCADE)
   run = models.ForeignKey(RunDetails, on_delete=models.CASCADE)

class Performance(models.Model):
    results = models.OneToOneField(Results, on_delete=models.CASCADE, related_name="performance")
    e2e_processed_tok_sec = models.CharField(max_length=100, blank=True)
    e2e_generated_tok_sec = models.CharField(max_length=100, blank=True)
    average_ttft_sec = models.CharField(max_length=100, blank=True)
    output_token_throughput = models.CharField(max_length=100, blank=True)
    mean_ttft_sec = models.CharField(max_length=100, blank=True)
    request_throughput = models.CharField(max_length=100, blank=True)
    total_token_throughput_tok_sec = models.CharField(max_length=100, blank=True)
