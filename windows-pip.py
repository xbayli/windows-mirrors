import requests
import time
from concurrent.futures import ThreadPoolExecutor

def test_latency(url):
    try:
        start_time = time.time()
        response = requests.get(url, timeout=1)
        end_time = time.time()
        if response.status_code == 200:
            latency = end_time - start_time
            return url, latency
    except requests.RequestException:
        pass
    return url, float('inf')

def speed_test_sources(sources):
    results = []
    total_sources = len(sources)

    def progress_callback(url, latency):
        results.append((url, latency))
        progress = len(results)
        print(f"Testing source {progress}/{total_sources} - {url} - 延迟为 {latency:.2f} 秒")

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(test_latency, url) for url in sources]
        for future in futures:
            url, latency = future.result()
            progress_callback(url, latency)

    sorted_sources = sorted(results, key=lambda x: x[1] if x[1] != float('inf') else float('inf'))

    return sorted_sources

def main():
    sources = [
        ("阿里云", "http://mirrors.aliyun.com/pypi/simple/"),
        ("中国科技大学", "https://pypi.mirrors.ustc.edu.cn/simple/"),
        ("豆瓣", "http://pypi.douban.com/simple/"),
        ("清华大学", "https://pypi.tuna.tsinghua.edu.cn/simple/"),
        ("中国科学技术大学", "http://pypi.mirrors.ustc.edu.cn/simple/"),
        ("腾讯云","https://mirrors.cloud.tencent.com/pypi/simple/"),
        ("华中科技大学","http://pypi.hustunique.com/"),
        ("华南理工大学","http://pypi.sustech.edu.cn/simple/"),
        ("PyPI","https://pypi.org/simple/"),
        ("Fastly CDN 全球加速","https://pypi.org/simple/"),
        ("Amazon S3 全球加速","https://pypi.fury.io/simple/"),
        ("Google Cloud Storage 全球加速","https://storage.googleapis.com/pypi.simple/"),
        ("Microsoft Azure 全球加速","https://pkgs.dev.azure.com/yourorg/simple/")
    ]

    print("可用源列表:")
    for index, (name, url) in enumerate(sources):
        print(f"{index + 1}. {name} {url}")

    speed_test_choice = input("是否进行速度测试？(y/n，默认为不测试)：").strip().lower()

    if speed_test_choice == 'y':
        sorted_sources = speed_test_sources([url for _, url in sources])
        print("\n按延迟从低到高的顺序显示这些源：")
        for index, (url, latency) in enumerate(sorted_sources):  # 修改这里，使用enumerate函数
            if latency != float('inf'):
                print(f"{index + 1}. {url} 的延迟为: {latency:.2f} 秒")
            else:
                print(f"{index + 1}. {url} - 连接超时")

        selected_source_index = input("请输入数字选择源：")
    else:
        print("\n请选择一个源进行设置：")
        for index, (name, url) in enumerate(sources):
            print(f"{index + 1}. {name} {url}")

        selected_source_index = input("请输入数字选择源：")

    while not selected_source_index.isdigit() or int(selected_source_index) < 1 or int(selected_source_index) > len(sources):
        print("无效的选择，请重新输入数字选择源：")
        selected_source_index = input("请输入数字选择源：")

    selected_source = sources[int(selected_source_index) - 1][1]
    print(f"已选择源：{selected_source}")

    input("按 Enter 退出")

if __name__ == "__main__":
    main()
