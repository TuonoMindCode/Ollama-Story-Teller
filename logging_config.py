import os
import glob
import datetime

class LoggingConfig:
    def __init__(self, settings_manager, stories_folder):
        """
        Initialize with settings manager and stories folder path
        """
        self.settings = settings_manager
        self.stories_folder = stories_folder
        
    def configure_logging_settings(self):
        """Configure detailed logging settings with explanations"""
        while True:
            print("\n" + "="*70)
            print("PROMPT LOGGING & DEBUGGING")
            print("="*70)
            
            # Explanation section
            print("WHAT IS PROMPT LOGGING?")
            print("-" * 70)
            print("Prompt logging records every conversation between this app and Ollama")
            print("to help you understand and improve story generation quality.")
            print()
            print("WHAT GETS LOGGED:")
            print("• System Prompt - Instructions given to the AI model")
            print("• User Prompt - The actual story generation request")
            print("• Ollama Response - What the AI model generated")
            print("• Timing & Token information")
            print()
            print("WHY USE LOGGING?")
            print("• Debug why stories aren't turning out as expected")
            print("• See if Ollama is following your system prompts correctly")
            print("• Identify if your chosen model is suitable for your needs")
            print("• Fine-tune prompts for better story quality")
            print()
            print("IMPORTANT NOTES:")
            print("• Log files can become very large (several MB per story)")
            print("• Logs contain the full text of generated stories")
            print("• Only enable if you need to troubleshoot story generation")
            print("• Logs are stored in the 'logs/' folder")
            
            print("\n" + "="*70)
            print("CURRENT SETTINGS:")
            print("="*70)
            
            enabled = self.settings.get("enable_prompt_logging", False)
            detailed = self.settings.get("detailed_logging", True)
            retention = self.settings.get("log_retention_days", 30)
            
            # Show current status with better formatting
            status_text = "ENABLED" if enabled else "DISABLED"
            print(f"Logging Status: {status_text}")
            
            if enabled:
                mode_text = "Full prompts & responses" if detailed else "Summary only"
                print(f"Logging Detail: {mode_text}")
                
                retention_text = "Keep forever" if retention == 0 else f"Keep for {retention} days"
                print(f"Log Retention: {retention_text}")
                
                # Show current log file count and size
                try:
                    logs_dir = os.path.join(os.path.dirname(self.stories_folder), 'logs')
                    if os.path.exists(logs_dir):
                        log_files = glob.glob(os.path.join(logs_dir, 'prompt_log_*.txt'))
                        if log_files:
                            total_size = sum(os.path.getsize(f) for f in log_files)
                            print(f"Current Logs: {len(log_files)} files, {self._format_size(total_size)}")
                        else:
                            print(f"Current Logs: No log files found")
                except:
                    pass
            
            print("\n" + "="*70)
            print("OPTIONS:")
            print("="*70)
            print("1. Enable/Disable Logging")
            print("2. Set Logging Detail Level")
            print("3. Configure Log Retention")
            print("4. View Current Log Files")
            print("5. Clean Up Old Logs")
            print("6. Back to Advanced Settings")
            
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == "1":
                self._toggle_prompt_logging()
                
            elif choice == "2":
                if not enabled:
                    print("\nLogging is currently disabled. Enable it first to configure detail level.")
                    input("Press Enter to continue...")
                    continue
                self._configure_logging_detail()
                
            elif choice == "3":
                if not enabled:
                    print("\nLogging is currently disabled. Enable it first to configure retention.")
                    input("Press Enter to continue...")
                    continue
                self._configure_log_retention()
                
            elif choice == "4":
                self._view_log_files()
                
            elif choice == "5":
                self._cleanup_logs_menu()
                
            elif choice == "6":
                break
            else:
                print("Invalid option")
                input("Press Enter to continue...")

    def _toggle_prompt_logging(self):
        """Toggle prompt logging with detailed explanation"""
        current = self.settings.get("enable_prompt_logging", False)
        
        if current:
            print("\nDISABLE LOGGING")
            print("-" * 50)
            print("This will stop recording prompt exchanges.")
            print("Existing log files will be kept unless you delete them manually.")
            confirm = input("\nDisable logging? (y/n): ").strip().lower()
            if confirm == 'y':
                self.settings.set("enable_prompt_logging", False)
                print("Prompt logging disabled")
            else:
                print("Cancelled")
        else:
            print("\nENABLE LOGGING")
            print("-" * 50)
            print("This will start recording all prompt exchanges.")
            print()
            print("What will be logged:")
            print("• Every system prompt sent to Ollama")
            print("• Every story generation request")
            print("• Ollama's complete responses")
            print("• Model settings and parameters")
            print()
            print("Storage impact:")
            print("• Each story generation creates ~1-5MB of logs")
            print("• Logs are stored in text files in the 'logs/' folder")
            print("• You can configure automatic cleanup")
            print()
            print("Best used for:")
            print("• Troubleshooting poor story quality")
            print("• Testing different models or settings")
            print("• Understanding how prompts affect output")
            
            confirm = input("\nEnable logging? (y/n): ").strip().lower()
            if confirm == 'y':
                self.settings.set("enable_prompt_logging", True)
                print("Prompt logging enabled")
                print("Logs will be created starting with your next story generation")
            else:
                print("Cancelled")
        
        input("Press Enter to continue...")

    def _configure_logging_detail(self):
        """Configure how detailed the logging should be"""
        current = self.settings.get("detailed_logging", True)
        
        print("\nLOGGING DETAIL LEVEL")
        print("-" * 50)
        
        if current:
            print("Current: FULL LOGGING")
            print("• Records complete system prompts")
            print("• Records complete user prompts") 
            print("• Records complete Ollama responses")
            print("• Includes formatted boxes for easy reading")
            print("• Larger file sizes (~3-5MB per story)")
            print()
            print("Switch to SUMMARY LOGGING?")
            print("• Records only prompt lengths and previews")
            print("• Much smaller files (~100KB per story)")
            print("• Good for basic troubleshooting")
        else:
            print("Current: SUMMARY LOGGING")
            print("• Records prompt lengths and short previews")
            print("• Smaller file sizes (~100KB per story)")
            print("• Basic troubleshooting information")
            print()
            print("Switch to FULL LOGGING?")
            print("• Records complete prompts and responses")
            print("• Detailed analysis capabilities")
            print("• Larger files (~3-5MB per story)")
        
        confirm = input(f"\nSwitch to {'SUMMARY' if current else 'FULL'} logging? (y/n): ").strip().lower()
        if confirm == 'y':
            new_value = not current
            self.settings.set("detailed_logging", new_value)
            mode = "FULL" if new_value else "SUMMARY"
            print(f"Logging detail level set to: {mode}")
        else:
            print("No changes made")
        
        input("Press Enter to continue...")

    def _configure_log_retention(self):
        """Configure how long to keep log files"""
        current = self.settings.get("log_retention_days", 30)
        
        print("\nLOG RETENTION SETTINGS")
        print("-" * 50)
        print(f"Current setting: {'Keep forever' if current == 0 else f'Keep for {current} days'}")
        print()
        print("Log retention automatically deletes old log files to save disk space.")
        print()
        print("Recommended settings:")
        print("• 7 days - For casual users who just want recent debugging info")
        print("• 30 days - Good balance of history and disk space")
        print("• 90 days - For users who frequently reference old logs")
        print("• 0 - Keep forever (manual cleanup only)")
        
        try:
            days = input("\nEnter days to keep logs (0 = keep forever): ").strip()
            days = int(days)
            if days >= 0:
                self.settings.set("log_retention_days", days)
                if days == 0:
                    print("Logs will be kept forever")
                    print("  You can still manually clean them up from the menu")
                else:
                    print(f"Logs will be automatically deleted after {days} days")
            else:
                print("Please enter 0 or a positive number")
        except ValueError:
            print("Please enter a valid number")
        
        input("Press Enter to continue...")

    def _view_log_files(self):
        """Show information about current log files"""
        try:
            logs_dir = os.path.join(os.path.dirname(self.stories_folder), 'logs')
            if not os.path.exists(logs_dir):
                print("\nNo logs directory found")
                print("Logs will be created when you generate stories with logging enabled.")
                input("Press Enter to continue...")
                return
            
            log_files = glob.glob(os.path.join(logs_dir, 'prompt_log_*.txt'))
            
            if not log_files:
                print("\nNo log files found")
                print("Logs will be created when you generate stories with logging enabled.")
                input("Press Enter to continue...")
                return
            
            print(f"\n LOG FILES SUMMARY")
            print("="*60)
            print(f"Found {len(log_files)} log file(s) in: {logs_dir}")
            print()
            
            # Sort by modification time (newest first)
            log_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            
            total_size = 0
            for i, log_file in enumerate(log_files, 1):
                size = os.path.getsize(log_file)
                total_size += size
                modified = datetime.datetime.fromtimestamp(os.path.getmtime(log_file))
                
                filename = os.path.basename(log_file)
                age_days = (datetime.datetime.now() - modified).days
                
                print(f"{i:2d}. {filename}")
                print(f"    Size: {self._format_size(size):>8} | Age: {age_days} days | Modified: {modified.strftime('%Y-%m-%d %H:%M')}")
            
            print(f"\nTotal log size: {self._format_size(total_size)}")
            
            print(f"\nTIP: Log files are plain text and can be opened with any text editor")
            print(f"    Location: {logs_dir}")
            
        except Exception as e:
            print(f"Error viewing log files: {e}")
            
        input("\nPress Enter to continue...")

    def _cleanup_logs_menu(self):
        """Menu for cleaning up log files"""
        try:
            logs_dir = os.path.join(os.path.dirname(self.stories_folder), 'logs')
            if not os.path.exists(logs_dir):
                print("\nNo logs directory found - nothing to clean up")
                input("Press Enter to continue...")
                return
            
            log_files = glob.glob(os.path.join(logs_dir, 'prompt_log_*.txt'))
            
            if not log_files:
                print("\nNo log files found - nothing to clean up")
                input("Press Enter to continue...")
                return
            
            # Calculate total size
            total_size = sum(os.path.getsize(f) for f in log_files)
            
            print(f"\nLOG CLEANUP")
            print("="*50)
            print(f"Found {len(log_files)} log file(s)")
            print(f"Total size: {self._format_size(total_size)}")
            print()
            print("WARNING: This action cannot be undone!")
            print("Make sure you don't need these logs for debugging.")
            print()
            
            confirm = input("Delete ALL log files? (type 'DELETE' to confirm): ").strip()
            if confirm == 'DELETE':
                deleted = 0
                freed_space = 0
                for log_file in log_files:
                    try:
                        size = os.path.getsize(log_file)
                        os.remove(log_file)
                        deleted += 1
                        freed_space += size
                    except OSError as e:
                        print(f"Could not delete {os.path.basename(log_file)}: {e}")
                
                print(f"Deleted {deleted} log file(s)")
                print(f"Freed {self._format_size(freed_space)} of disk space")
            else:
                print("Cleanup cancelled")
                
        except Exception as e:
            print(f"Error during cleanup: {e}")
            
        input("Press Enter to continue...")

    def _format_size(self, size_bytes):
        """Convert bytes to human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        # Define size units
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        
        # Find the appropriate unit
        unit_index = 0
        size = float(size_bytes)
        
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        
        # Format with appropriate decimal places
        if unit_index == 0:  # Bytes
            return f"{int(size)} {units[unit_index]}"
        elif size >= 100:  # 100+ MB/GB etc
            return f"{size:.0f} {units[unit_index]}"
        elif size >= 10:   # 10-99 MB/GB etc  
            return f"{size:.1f} {units[unit_index]}"
        else:              # Less than 10 MB/GB etc
            return f"{size:.2f} {units[unit_index]}"
