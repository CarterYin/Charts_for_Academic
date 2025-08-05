import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# 设置英文字体
# plt.rcParams['font.family'] = 'Arial'
# 设置中文字体，优先使用常见的中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

print("Reading data...")
df = pd.read_csv('analysis_result_eyes_realigned.tsv', sep='\t')

# 种族ID到名字的映射
# ethnic_mapping = {
#     1: 'Han', 2: 'Mongol', 3: 'Hui', 4: 'Zang', 5: 'Uygur', 6: 'Miao', 7: 'Yi', 8: 'Zhuang', 9: 'Buyei',
#     10: 'Chosen', 11: 'Man', 12: 'Dong', 13: 'Yao', 14: 'Bai', 15: 'Tujia', 16: 'Hani', 17: 'Kazak', 18: 'Dai',
#     19: 'Li', 20: 'Lisu', 21: 'Va', 22: 'She', 23: 'Gaoshan', 24: 'Lahu', 25: 'Sui', 26: 'Dongxiang', 27: 'Naxi',
#     28: 'Jingpo', 29: 'Kirgiz', 30: 'Tu', 31: 'Daur', 32: 'Mulao', 33: 'Qiang', 34: 'Blang', 35: 'Salar',
#     36: 'Maonan', 37: 'Gelao', 38: 'Xibe', 39: 'Achang', 40: 'Pumi', 41: 'Tajik', 42: 'Nu', 43: 'Uzbek',
#     44: 'Russ', 45: 'Ewenki', 46: 'Maonan', 47: 'Bonan', 48: 'Yugur', 49: 'Gin', 50: 'Tatar', 51: 'Derung',
#     52: 'Oroqen', 53: 'Hezhen', 54: 'Monba', 55: 'Lhoba', 56: 'Jino', 97: 'Other', 98: 'Foreigner'
# }
ethnic_mapping = {
    1: '汉族', 2: '蒙古族', 3: '回族', 4: '藏族', 5: '维吾尔族', 6: '苗族', 7: '彝族', 8: '壮族', 9: '布依族',
    10: '朝鲜族', 11: '满族', 12: '侗族', 13: '瑶族', 14: '白族', 15: '土家族', 16: '哈尼族', 17: '哈萨克族', 18: '傣族',
    19: '黎族', 20: '傈僳族', 21: '佤族', 22: '畲族', 23: '高山族', 24: '拉祜族', 25: '水族', 26: '东乡族', 27: '纳西族',
    28: '景颇族', 29: '柯尔克孜族', 30: '土族', 31: '达斡尔族', 32: '仫佬族', 33: '羌族', 34: '布朗族', 35: '撒拉族',
    36: '毛难族', 37: '仡佬族', 38: '锡伯族', 39: '阿昌族', 40: '普米族', 41: '塔吉克族', 42: '怒族', 43: '乌孜别克族',
    44: '俄罗斯族', 45: '鄂温克族', 46: '崩龙族', 47: '保安族', 48: '裕固族', 49: '京族', 50: '塔塔尔族', 51: '独龙族',
    52: '鄂伦春族', 53: '赫哲族', 54: '门巴族', 55: '珞巴族', 56: '基诺族', 57: '其他', 58: '外国血统'
}

# 疾病分组
disease_cols_group1 = {
    'glaucoma_diag': 'Glaucoma',
    'amd_diag': 'AMD',
    'cataract_diag': 'Cataract'
}

disease_cols_group2 = {
    'diabetes_test': 'Diabetes',
    'ihd_diag': 'IHD',
    'peri_art_dis_symptoms': 'Peri-articular Symptoms',
    'pre_18_pneu_bronch_tb': 'Pre-18 Pneumonia/Bronchitis/TB'
}

def calculate_prevalence(df, disease_cols):
    results = []
    ethnic_groups = sorted(df['id_ethnic_group_id'].unique())
    for ethnic in ethnic_groups:
        ethnic_df = df[df['id_ethnic_group_id'] == ethnic]
        for col, name in disease_cols.items():
            if col in df.columns:
                valid_data = ethnic_df[ethnic_df[col].notna()]
                if len(valid_data) > 0:
                    cases = valid_data[col].sum()
                    total = len(valid_data)
                    prevalence = (cases / total * 100) if total > 0 else 0
                    results.append({
                        'ethnic_group': ethnic,
                        'disease': name,
                        'prevalence': round(prevalence, 2)
                    })
    return pd.DataFrame(results)

prevalence_data_group1 = calculate_prevalence(df, disease_cols_group1)
prevalence_data_group2 = calculate_prevalence(df, disease_cols_group2)

# 配色
disease_colors_group1 = ['peachpuff', 'plum', 'purple']
disease_colors_group2 = ['yellowgreen', 'wheat', 'lightpink', '#f737ba']

# Group 1 疾病直方图（眼病）
fig1, ax1 = plt.subplots(figsize=(18, 12))
data_group1_filtered = prevalence_data_group1
pivot_data1 = data_group1_filtered.pivot(index='ethnic_group', columns='disease', values='prevalence').fillna(0)
pivot_data1 = pivot_data1[['Glaucoma', 'AMD', 'Cataract']]
x = np.arange(len(pivot_data1.index))
width = 0.25
diseases_order = ['Glaucoma', 'AMD', 'Cataract']
for i, disease in enumerate(diseases_order):
    if disease in pivot_data1.columns:
        values = pivot_data1[disease]
        offset = width * i - width
        bars = ax1.bar(x + offset, values, width, label=disease, color=disease_colors_group1[i])

ax1.set_xlabel('Ethnic Group', fontsize=16, fontweight='bold')
ax1.set_ylabel('Prevalence (%)', fontsize=16, fontweight='bold')
ax1.set_title('Eye Diseases Prevalence by Ethnic Group', fontsize=20, fontweight='bold', pad=20)
ax1.set_xticks(x)
ax1.set_xticklabels([ethnic_mapping.get(int(i), f'ID {int(i)}') for i in pivot_data1.index], rotation=45, ha='center', fontsize=12)
ax1.legend(bbox_to_anchor=(1.02, 0.5), loc='center left', fontsize=14, frameon=False, handlelength=1.5, handleheight=1.5)
ax1.grid(True, axis='y', alpha=0.3)
ax1.tick_params(axis='x', which='both', length=0)
ax1.tick_params(axis='y', which='both', length=0)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.spines['left'].set_visible(False)
plt.tight_layout()
plt.savefig('eye_diseases_bar.png', dpi=1200, bbox_inches='tight', facecolor='white')
plt.close()

# Group 2 疾病直方图（其他疾病）
fig2, ax2 = plt.subplots(figsize=(18, 12))
data_group2_filtered = prevalence_data_group2
pivot_data2 = data_group2_filtered.pivot(index='ethnic_group', columns='disease', values='prevalence').fillna(0)
x = np.arange(len(pivot_data2.index))
width = 0.2
for i, (disease, values) in enumerate(pivot_data2.items()):
    offset = width * i - width*1.5
    bars = ax2.bar(x + offset, values, width, label=disease, color=disease_colors_group2[i])

ax2.set_xlabel('Ethnic Group', fontsize=16, fontweight='bold')
ax2.set_ylabel('Prevalence (%)', fontsize=16, fontweight='bold')
ax2.set_title('Other Diseases Prevalence by Ethnic Group', fontsize=20, fontweight='bold', pad=20)
ax2.set_xticks(x)
ax2.set_xticklabels([ethnic_mapping.get(int(i), f'ID {int(i)}') for i in pivot_data2.index], rotation=45, ha='center', fontsize=12)
ax2.legend(bbox_to_anchor=(1.02, 0.5), loc='center left', fontsize=14, frameon=False, handlelength=1.5, handleheight=1.5)
ax2.grid(True, axis='y', alpha=0.3)
ax2.tick_params(axis='x', which='both', length=0)
ax2.tick_params(axis='y', which='both', length=0)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.spines['left'].set_visible(False)
plt.tight_layout()
plt.savefig('other_diseases_bar.png', dpi=1200, bbox_inches='tight', facecolor='white')
plt.close()

print("\n直方图绘制完成！")
print("\n生成文件：")
print("1. eye_diseases_bar.png - 眼病患病率直方图")
print("2. other_diseases_bar.png - 其他疾病患病率直方图") 