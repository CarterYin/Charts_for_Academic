import pandas as pd
import matplotlib.pyplot as plt

# 设置英文字体
# plt.rcParams['font.family'] = 'Arial'
# 设置中文字体，优先使用常见的中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

def plot_exclude_max_histogram(tsv_file_path, column_name='id_ethnic_group_id'):
    """
    读取TSV文件并绘制除了最大数据的其他数据的直方图
    
    参数:
    tsv_file_path: TSV文件路径
    column_name: 要分析的列名，默认为'id_ethnic_group_id'
    """
    
    try:
        # 读取TSV文件
        print(f"正在读取文件: {tsv_file_path}")
        df = pd.read_csv(tsv_file_path, sep='\t')
        
        print(f"文件读取成功！数据形状: {df.shape}")
        
        # 检查指定列是否存在
        if column_name not in df.columns:
            print(f"错误: 列 '{column_name}' 不存在于文件中")
            return
        
        # 获取指定列的数据
        data = df[column_name]
        
        print(f"\n{column_name} 列的基本信息:")
        print(f"非空值数量: {data.count()}")
        print(f"缺失值数量: {data.isnull().sum()}")
        
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
        # 计算每个种族ID的数量
        value_counts = data.value_counts().sort_index()
        
        print(f"\n原始数据统计:")
        print(f"最大值: {value_counts.max()}")
        print(f"最大值对应的种族ID: {value_counts.idxmax()}")
        print(f"总种族数量: {len(value_counts)}")
        
        # 排除最大值
        value_counts_exclude_max = value_counts[value_counts != value_counts.max()]
        
        print(f"\n排除最大值后的统计:")
        print(f"剩余种族数量: {len(value_counts_exclude_max)}")
        print(f"排除的数据量: {value_counts.max()}")
        
        # 创建条形图
        plt.figure(figsize=(12, 6))
        
        # 绘制条形图
        bars = plt.bar(range(len(value_counts_exclude_max)), value_counts_exclude_max.values, alpha=0.7, color='#d2b48c', edgecolor='white')
        
        # 为每个条形添加数据标签
        for i, (bar, count) in enumerate(zip(bars, value_counts_exclude_max.values)):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{int(count)}', ha='center', va='bottom', 
                    fontsize=8, color='black', fontweight='normal')
        
        plt.xlabel('Ethnic Group', fontsize=12)
        plt.ylabel('Number of Candidates', fontsize=12)
        # plt.title(f'Ethnic Group Distribution (Excluding Max: {value_counts.max()} from ID {value_counts.idxmax()})', fontsize=14, fontweight='bold')
        
        # 设置横轴标签为种族名字，并去掉刻度线
        ethnic_names = [ethnic_mapping.get(int(x), f'ID {int(x)}') for x in value_counts_exclude_max.index]
        plt.xticks(range(len(value_counts_exclude_max)), ethnic_names, rotation=45, ha='center')
        plt.tick_params(axis='x', which='both', length=0)
        plt.tick_params(axis='y', which='both', length=0)
        
        # 只保留网格线的横线，去掉所有边框和网格线竖线
        plt.grid(True, axis='y', alpha=0.3)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        
        plt.tight_layout()
        
        # 保存超高像素图片（在显示之前保存）
        plt.savefig('exclude_max_histogram_ultra_high.png', dpi=1200, bbox_inches='tight', facecolor='white')
        
        plt.show()
        
        # 打印详细统计信息
        print(f"\n{column_name} 的基本统计（排除最大值后）:")
        print(value_counts_exclude_max.describe())
        
        print(f"\n{column_name} 的值计数（排除最大值后）:")
        print(value_counts_exclude_max)
        
        # 计算百分比
        total_exclude_max = value_counts_exclude_max.sum()
        percentages = (value_counts_exclude_max / total_exclude_max * 100).round(2)
        print(f"\n{column_name} 的百分比分布（排除最大值后）:")
        for value, percentage in percentages.items():
            print(f"  {value}: {percentage}%")
            
    except FileNotFoundError:
        print(f"错误: 找不到文件 {tsv_file_path}")
    except Exception as e:
        print(f"读取文件时发生错误: {str(e)}")

if __name__ == "__main__":
    # 文件路径
    tsv_file = "analysis_result_eyes_realigned.tsv"
    
    # 绘制排除最大值的直方图
    plot_exclude_max_histogram(tsv_file, 'id_ethnic_group_id') 