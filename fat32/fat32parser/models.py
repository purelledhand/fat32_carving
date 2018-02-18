from django.db import models
from django.utils import timezone
# Create your models here.

class Carving(models.Model):
	bytes_per_sector = models.IntegerField()
	sectors_per_cluster = models.IntegerField()
	reserved = models.IntegerField()
	fat32_size = models.IntegerField()
	cluster_size = models.IntegerField()
	FAT1 = models.IntegerField()
	FAT2 = models.IntegerField()
	Root_Directory = models.IntegerField()
"""
	def cluster_size(self):
		return bytes_per_sector*sectors_per_cluster

	def FAT1(self):
		return reserved

	def FAT2(self):
		return FAT1()+fat32_size

	def Root_Directory(self):
		return FAT2()+fat32_size
"""