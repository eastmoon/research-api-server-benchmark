# 使用 #@DESC 描述此模組的用途
# 模組對於基礎設施定義檔處理流程與參數解析說明描述於 desc 函數
#@DESC Simple module structure, and run standard command.

# Import libraries
from libs.docker import Service
# Declare variable
# Declare function
def main():
    """
    ISA 系統不會呼叫該函數，此函數應用於單獨執行時，用來測試模組內容
    """

def desc():
    """
    用於描述當前模組對配置內容的處理規則。
    """
    print("This module is run for standard command.")

def exec(config):
    """
    模組執行時最後呼叫的函數，可在此執行配置檔中無特定對應函數的內容
    """
    print("Execute module with config.")
    s = Service(config, exec.__module__)
    s.run()

# Python entrypoint program
if __name__ == '__main__':
    main()
