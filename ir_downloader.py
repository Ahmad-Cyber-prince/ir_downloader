#!/usr/bin/env python3
"""
🚀 IR DOWNLOADER - Ultimate Cross-Platform Download Manager
📱 Created by Ahmad Cyber Prince
🔗 https://github.com/Ahmad-Cyber-prince
🌍 Supports: Windows, macOS, Linux, Android, iOS
"""

import requests
import os
import time
import sys
import platform
import subprocess
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

# رنگ‌های سازگار با همه ترمینال‌ها
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # رنگ‌های اصلی
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

class CrossPlatformManager:
    """مدیریت سازگاری با تمام پلتفرم‌ها"""
    
    @staticmethod
    def detect_platform():
        """تشخیص خودکار پلتفرم"""
        system = platform.system().lower()
        
        # تشخیص محیط‌های خاص
        if 'termux' in sys.executable.lower() or 'android' in system:
            return 'android'
        elif 'pythonista' in sys.executable.lower():
            return 'ios'
        else:
            return system  # windows, darwin, linux
    
    @staticmethod
    def get_download_directory():
        """دریافت مسیر دانلود مناسب برای هر پلتفرم"""
        platform_type = CrossPlatformManager.detect_platform()
        home = Path.home()
        
        download_dirs = {
            'windows': home / 'Downloads' / 'IR_Downloads',
            'darwin': home / 'Downloads' / 'IR_Downloads',  # macOS
            'linux': home / 'Downloads' / 'IR_Downloads',
            'android': Path('/storage/emulated/0/Download/IR_Downloads'),
            'ios': home / 'Documents' / 'IR_Downloads',
        }
        
        download_dir = download_dirs.get(platform_type, home / 'IR_Downloads')
        
        # ایجاد دایرکتوری اگر وجود ندارد
        download_dir.mkdir(parents=True, exist_ok=True)
        return download_dir
    
    @staticmethod
    def get_platform_info():
        """دریافت اطلاعات کامل پلتفرم"""
        platform_type = CrossPlatformManager.detect_platform()
        
        info = {
            'platform': platform_type,
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
        }
        
        return info

class IRDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.platform_manager = CrossPlatformManager()
        self.platform_info = self.platform_manager.get_platform_info()
        
        # تنظیم User-Agent مناسب
        user_agents = {
            'windows': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'darwin': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'linux': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'android': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36',
            'ios': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36'
        }
        
        user_agent = user_agents.get(
            self.platform_info['platform'],
            'Mozilla/5.0 (compatible; IR-Downloader/1.0)'
        )
        
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
        })
        
        # دریافت مسیر دانلود
        self.download_dir = self.platform_manager.get_download_directory()
        
        # آمارگیری
        self.download_stats = {
            'total_downloads': 0,
            'total_size': 0,
            'start_time': datetime.now()
        }
        
        # پاکسازی صفحه و نمایش اطلاعات
        self.clear_screen()
        self.show_banner()
        self.show_system_info()
    
    def clear_screen(self):
        """پاکسازی صفحه ترمینال"""
        try:
            if os.name == 'nt':  # Windows
                os.system('cls')
            else:  # Unix/Linux/Mac/Android
                os.system('clear')
        except:
            # Fallback: چاپ چند خط خالی
            print('\n' * 50)
    
    def show_banner(self):
        """نمایش بنر زیبا"""
        banner = f"""
{Colors.CYAN}{Colors.BOLD}
                         ___                                      ___                         ___                       
 .-.                    (   )                                    (   )                       (   )                      
( __)  ___ .-.        .-.| |    .--.    ___  ___  ___  ___ .-.    | |    .--.     .---.    .-.| |    .--.    ___ .-.    
(''") (   )   \      /   \ |   /    \  (   )(   )(   )(   )   \   | |   /    \   / .-, \  /   \ |   /    \  (   )   \   
 | |   | ' .-. ;    |  .-. |  |  .-. ;  | |  | |  | |  |  .-. .   | |  |  .-. ; (__) ; | |  .-. |  |  .-. ;  | ' .-. ;  
 | |   |  / (___)   | |  | |  | |  | |  | |  | |  | |  | |  | |   | |  | |  | |   .'`  | | |  | |  |  | | |  |  / (___) 
 | |   | |          | |  | |  | |  | |  | |  | |  | |  | |  | |   | |  | |  | |  / .'| | | |  | |  |  |/  |  | |        
 | |   | |          | |  | |  | |  | |  | |  | |  | |  | |  | |   | |  | |  | | | /  | | | |  | |  |  ' _.'  | |        
 | |   | |          | '  | |  | '  | |  | |  ; '  | |  | |  | |   | |  | '  | | ; |  ; | | '  | |  |  .'.-.  | |        
 | |   | |          ' `-'  /  '  `-' /  ' `-'   `-' '  | |  | |   | |  '  `-' / ' `-'  | ' `-'  /  '  `-' /  | |        
(___) (___)          `.__,'    `.__.'    '.__.'.__.'  (___)(___) (___)  `.__.'  `.__.'_.  `.__,'    `.__.'  (___)       
                                                                                                                        
                                                                                                                        
{Colors.RESET}"""
        print(banner)
        
        # اطلاعات سازنده و پلتفرم
        platform_info = f"""
{Colors.GREEN}🚀 IR DOWNLOADER - {self.platform_info['system'].upper()} EDITION
{Colors.CYAN}📱 Created by: {Colors.YELLOW}Ahmad Cyber Prince
{Colors.CYAN}🔗 GitHub: {Colors.BLUE}https://github.com/Ahmad-Cyber-prince
{Colors.CYAN}🌍 Platform: {Colors.MAGENTA}{self.platform_info['system']} {self.platform_info['release']} ({self.platform_info['platform']})
{Colors.CYAN}🏗️ Architecture: {Colors.WHITE}{self.platform_info['machine']}
{Colors.CYAN}{'═' * 70}{Colors.RESET}
"""
        print(platform_info)
    
    def show_system_info(self):
        """نمایش اطلاعات سیستم"""
        print(f"{Colors.YELLOW}📊 System Information:{Colors.RESET}")
        print(f"{Colors.GREEN}✅ Download Directory: {Colors.WHITE}{self.download_dir}")
        print(f"{Colors.GREEN}✅ Python Version: {Colors.WHITE}{sys.version.split()[0]}")
        print(f"{Colors.GREEN}✅ Requests Version: {Colors.WHITE}{requests.__version__}")
        print(f"{Colors.CYAN}{'─' * 70}{Colors.RESET}")
    
    def get_file_info(self, url):
        """دریافت اطلاعات فایل"""
        try:
            print(f"{Colors.CYAN}🔍 Analyzing URL: {Colors.WHITE}{url}")
            
            response = self.session.head(url, timeout=10, allow_redirects=True)
            response.raise_for_status()
            
            content_type = response.headers.get('content-type', '')
            content_length = int(response.headers.get('content-length', 0))
            
            # استخراج نام فایل
            filename = self.extract_filename(url, response.headers)
            
            # تشخیص نوع فایل
            file_type = self.detect_file_type(content_type, filename)
            
            return {
                'filename': filename,
                'size': content_length,
                'type': file_type,
                'content_type': content_type,
                'url': url
            }
            
        except Exception as e:
            print(f"{Colors.RED}❌ Error analyzing URL: {Colors.WHITE}{e}")
            return {
                'filename': f"download_{int(time.time())}.bin",
                'size': 0,
                'type': 'Unknown',
                'content_type': '',
                'url': url
            }
    
    def extract_filename(self, url, headers):
        """استخراج نام فایل از URL یا هدرها"""
        # از Content-Disposition
        content_disp = headers.get('content-disposition', '')
        if 'filename=' in content_disp:
            filename = content_disp.split('filename=')[1].strip('"\'')
            if filename:
                return self.clean_filename(filename)
        
        # از URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        if not filename or filename == '/':
            ext = self.get_extension_from_type(headers.get('content-type', ''))
            filename = f"download_{int(time.time())}{ext}"
        
        return self.clean_filename(filename)
    
    def clean_filename(self, filename):
        """پاکسازی نام فایل برای پلتفرم فعلی"""
        import re
        invalid_chars = r'[<>:"/\\|?*]' if self.platform_info['platform'] in ['windows', 'android'] else r'[/]'
        cleaned = re.sub(invalid_chars, '_', filename)
        return cleaned
    
    def detect_file_type(self, content_type, filename):
        """تشخیص نوع فایل"""
        type_mapping = {
            'image/': '🖼️ Image',
            'video/': '🎥 Video',
            'audio/': '🎵 Audio',
            'text/': '📄 Text',
            'application/pdf': '📊 PDF',
            'application/zip': '📦 Archive',
        }
        
        for pattern, file_type in type_mapping.items():
            if content_type.startswith(pattern):
                return file_type
        
        # بررسی پسوند فایل
        ext = Path(filename).suffix.lower()
        ext_mapping = {
            '.jpg': '🖼️ Image', '.jpeg': '🖼️ Image', '.png': '🖼️ Image',
            '.gif': '🖼️ Image', '.webp': '🖼️ Image', '.bmp': '🖼️ Image',
            '.mp4': '🎥 Video', '.avi': '🎥 Video', '.mkv': '🎥 Video',
            '.mov': '🎥 Video', '.webm': '🎥 Video',
            '.mp3': '🎵 Audio', '.wav': '🎵 Audio', '.flac': '🎵 Audio',
            '.pdf': '📊 PDF', '.doc': '📄 Document', '.docx': '📄 Document',
            '.txt': '📄 Text', '.zip': '📦 Archive', '.rar': '📦 Archive',
            '.7z': '📦 Archive', '.tar': '📦 Archive',
        }
        
        return ext_mapping.get(ext, '📁 File')
    
    def get_extension_from_type(self, content_type):
        """دریافت پسوند از نوع محتوا"""
        ext_mapping = {
            'image/jpeg': '.jpg', 'image/jpg': '.jpg',
            'image/png': '.png', 'image/gif': '.gif',
            'image/webp': '.webp', 'image/bmp': '.bmp',
            'video/mp4': '.mp4', 'video/avi': '.avi',
            'video/x-matroska': '.mkv', 'video/quicktime': '.mov',
            'audio/mpeg': '.mp3', 'audio/wav': '.wav',
            'application/pdf': '.pdf', 'text/plain': '.txt',
            'application/zip': '.zip', 'application/x-rar-compressed': '.rar',
        }
        
        for pattern, ext in ext_mapping.items():
            if pattern in content_type:
                return ext
        
        return '.bin'
    
    def download_file(self, url, file_path, file_info):
        """دانلود فایل با نوار پیشرفت"""
        try:
            response = self.session.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            start_time = time.time()
            
            print(f"{Colors.CYAN}📥 Downloading {file_info['type']}: {Colors.WHITE}{file_info['filename']}")
            
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            bar_length = 40
                            filled = int(bar_length * percent / 100)
                            bar = '█' * filled + '░' * (bar_length - filled)
                            
                            elapsed = time.time() - start_time
                            speed = downloaded / elapsed / 1024 / 1024 if elapsed > 0 else 0
                            
                            print(f'\r{Colors.GREEN}[{bar}] {percent:6.1f}% | {speed:5.1f} MB/s', end='', flush=True)
            
            print(f'\r{Colors.GREEN}[{"█" * 40}] {Colors.GREEN}100.0% | Complete!{Colors.RESET}')
            return True
            
        except Exception as e:
            print(f"{Colors.RED}\n❌ Download error: {Colors.WHITE}{e}")
            return False
    
    def download(self, url):
        """متد اصلی دانلود"""
        # پاکسازی صفحه قبل از هر دانلود
        self.clear_screen()
        self.show_banner()
        
        # دریافت اطلاعات فایل
        file_info = self.get_file_info(url)
        
        print(f"{Colors.CYAN}📁 Filename: {Colors.WHITE}{file_info['filename']}")
        print(f"{Colors.BLUE}📊 Type: {Colors.WHITE}{file_info['type']}")
        if file_info['size'] > 0:
            print(f"{Colors.GREEN}💾 Size: {Colors.WHITE}{file_info['size']/1024/1024:.1f} MB")
        print(f"{Colors.YELLOW}🔗 Source: {Colors.WHITE}{url}")
        
        # تعیین مسیر فایل
        file_path = self.download_dir / file_info['filename']
        file_path = self.ensure_unique_filename(file_path)
        
        print(f"{Colors.MAGENTA}📂 Save path: {Colors.WHITE}{file_path}")
        print(f"{Colors.CYAN}{'─'*70}{Colors.RESET}")
        
        # شروع دانلود
        start_time = time.time()
        success = self.download_file(url, file_path, file_info)
        
        if success:
            # بروزرسانی آمار
            self.download_stats['total_downloads'] += 1
            if file_path.exists():
                file_size = file_path.stat().st_size
                self.download_stats['total_size'] += file_size
                
                download_time = time.time() - start_time
                avg_speed = file_size / download_time / 1024 / 1024
                
                self.show_success_message(file_path, file_size, download_time, avg_speed)
            return True
        else:
            print(f"{Colors.RED}❌ Download failed{Colors.RESET}")
            return False
    
    def ensure_unique_filename(self, file_path):
        """اطمینان از یکتا بودن نام فایل"""
        counter = 1
        original_stem = file_path.stem
        original_ext = file_path.suffix
        
        while file_path.exists():
            file_path = self.download_dir / f"{original_stem}_{counter}{original_ext}"
            counter += 1
        
        return file_path
    
    def show_success_message(self, file_path, file_size, download_time, avg_speed):
        """نمایش پیام موفقیت"""
        print(f"\n{Colors.GREEN}✅ Download Completed Successfully!")
        print(f"{Colors.CYAN}📁 File: {Colors.WHITE}{file_path.name}")
        print(f"{Colors.BLUE}📊 Size: {Colors.WHITE}{file_size/1024/1024:.2f} MB")
        print(f"{Colors.GREEN}⏱️ Time: {Colors.WHITE}{download_time:.1f} seconds")
        print(f"{Colors.YELLOW}🚀 Speed: {Colors.WHITE}{avg_speed:.1f} MB/s")
        print(f"{Colors.MAGENTA}📂 Location: {Colors.WHITE}{file_path}")
        print(f"{Colors.CYAN}{'═'*70}{Colors.RESET}")
    
    def show_stats(self):
        """نمایش آمار دانلود"""
        # پاکسازی صفحه قبل از نمایش آمار
        self.clear_screen()
        self.show_banner()
        
        total_time = datetime.now() - self.download_stats['start_time']
        
        print(f"{Colors.CYAN}📊 Download Statistics:{Colors.RESET}")
        print(f"{Colors.GREEN}📈 Total Downloads: {Colors.WHITE}{self.download_stats['total_downloads']}")
        print(f"{Colors.BLUE}💾 Total Size: {Colors.WHITE}{self.download_stats['total_size']/1024/1024:.2f} MB")
        print(f"{Colors.YELLOW}⏱️ Session Duration: {Colors.WHITE}{str(total_time).split('.')[0]}")
        print(f"{Colors.MAGENTA}📁 Download Directory: {Colors.WHITE}{self.download_dir}")
        print(f"{Colors.CYAN}{'═'*70}{Colors.RESET}")

def main():
    """تابع اصلی"""
    try:
        downloader = IRDownloader()
        
        while True:
            print(f"{Colors.CYAN}\n🎯 {'─'*50} 🎯{Colors.RESET}")
            url = input(f"{Colors.YELLOW}🌐 Enter URL (or 'exit' to quit, 'stats' for statistics): {Colors.RESET}").strip()
            
            if url.lower() in ['exit', 'quit', 'q']:
                downloader.show_stats()
                print(f"{Colors.GREEN}\n🙏 Thank you for using IR Downloader!")
                print(f"{Colors.CYAN}🔗 https://github.com/Ahmad-Cyber-prince{Colors.RESET}")
                break
            elif url.lower() == 'stats':
                downloader.show_stats()
                continue
            elif url.startswith(('http://', 'https://')):
                downloader.download(url)
            else:
                print(f"{Colors.RED}❌ URL must start with http:// or https://")
                print(f"{Colors.YELLOW}💡 Example: https://example.com/file.zip{Colors.RESET}")
                
    except KeyboardInterrupt:
        print(f"{Colors.RED}\n\n⏹️ Download interrupted by user{Colors.RESET}")
        if 'downloader' in locals():
            downloader.show_stats()
    except Exception as e:
        print(f"{Colors.RED}\n❌ Unexpected error: {e}{Colors.RESET}")

if __name__ == "__main__":
    main()
