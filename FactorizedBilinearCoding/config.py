#coding:utf-8
import warnings
warnings.filterwarnings('ignore')

class DefaultConfig(object):
	gpu_device = '2'
	#dataset 			#class 	train 	test
	DTD = False			#47 	3760 	1880
	CUB = False			#200 	5994 	5794
	INDOOR = False      #23 	51750 	5750
	MINC2500 = False	#	670		330
	MAD = True          # 2  18098  4535

	RANK_ATOMS = 1
	# RANK_ATOMS = 1  **
	NUM_CLUSTER = 4096
	BETA = 0.001
	model_name_pre = 'FBC'
	# model_path = None
	model_path = './tmp/28_FBC94.8181_lr_0.01.pth'  ## the path of the pretrained model
	save_low_bound = 79  ##when the accuracy achieves save_low_bound, the model is saved

	res_plus = 512
	# res_plus = 2048
	res = 224
	train_print_freq = 256	
	
	lr = 0.01
	lr_scale = 0.1
	lr_freq_list = [40,80]

	train_bs = 16
	down_chennel = 512
	# down_chennel = 2048
	test_bs = 2
	test_epoch = 1
	pretrained = True
	pre_path = 'data/vgg16-397923af.pth'
	# pre_path = 'data/resnet50-0676ba61.pth'

	model_name = 'FBC'
	use_gpu = True

	if MAD:
		data_path = 'data/mad-fingerprinting/few_shot_fingerprint/'
		train_txt_path = data_path + '1_FRLL_1_shot_train_list.txt'
		# set test files
		test_txt_path = data_path + '5_self_test_list.txt'
		# 1_FRLL_5_shot_train_list
		# 1_FRLL_1_shot_train_list
		# 1_FRLL_test_list
        # 2_FERET_1_shot_train_list
		# 2_FERET_5_shot_train_list
		# 2_FERET_test_list
		# 3_FRGC_1_shot_train_list
		# 3_FRGC_5_shot_train_list
		# 3_FRGC_test_list
		# 4_CelebA_1_shot_train_list
		# 4_CelebA_5_shot_train_list
		# 4_CelebA_test_list
		# 5_self_1_shot_train_list
		# 5_self_5_shot_train_list
		# 5_self_test_list
		# 6_all_1_shot_train_list
		# 6_all_5_shot_train_list
		# 6_all_test_list


		class_num = 9
		# class_num = 2   **
	else:
		print('data error')

	max_epoches = 150


opt = DefaultConfig()