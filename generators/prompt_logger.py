import os
from datetime import datetime, timedelta
import glob

class PromptLogger:
    def __init__(self, stories_folder, llm_settings, app_settings=None):
        self.stories_folder = stories_folder
        self.prompt_log_file = None
        self.llm_settings = llm_settings
        self.app_settings = app_settings or {}
        
        # Check if logging is enabled (default: False for most users)
        self.logging_enabled = self.app_settings.get("enable_prompt_logging", False)
        self.detailed_logging = self.app_settings.get("detailed_logging", True)
        self.log_retention_days = self.app_settings.get("log_retention_days", 30)
        
        if self.logging_enabled:
            self._initialize_prompt_logging(stories_folder)
            self._cleanup_old_logs()

    def _initialize_prompt_logging(self, stories_folder):
        """Initialize prompt logging file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_filename = f"prompt_log_{timestamp}.txt"
        
        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(os.path.dirname(stories_folder), 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        self.prompt_log_file = os.path.join(logs_dir, log_filename)
        
        # Write header
        with open(self.prompt_log_file, 'w', encoding='utf-8') as f:
            f.write(f"OLLAMA PROMPT LOG - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n")
            f.write(f"Model: {self.llm_settings.get('model', 'unknown')}\n")
            f.write(f"Temperature: {self.llm_settings.get('temperature', 0.7)}\n")
            f.write(f"Detailed Logging: {'Enabled' if self.detailed_logging else 'Summary Only'}\n")
            f.write("=" * 80 + "\n\n")
        
        print(f"📝 Prompt logging enabled: {log_filename}")

    def _cleanup_old_logs(self):
        """Remove old log files based on retention setting"""
        if self.log_retention_days <= 0:
            return  # Keep forever
        
        try:
            logs_dir = os.path.join(os.path.dirname(self.stories_folder), 'logs')
            if not os.path.exists(logs_dir):
                return
            
            cutoff_date = datetime.now() - timedelta(days=self.log_retention_days)
            log_files = glob.glob(os.path.join(logs_dir, 'prompt_log_*.txt'))
            
            deleted_count = 0
            for log_file in log_files:
                try:
                    file_time = datetime.fromtimestamp(os.path.getmtime(log_file))
                    if file_time < cutoff_date:
                        os.remove(log_file)
                        deleted_count += 1
                except (OSError, ValueError):
                    continue
            
            if deleted_count > 0:
                print(f"🧹 Cleaned up {deleted_count} old log file(s)")
                
        except Exception as e:
            print(f"⚠️ Error cleaning up logs: {e}")

    def log_prompt_exchange(self, stage, system_prompt, user_prompt, response, max_tokens):
        """Log the complete prompt exchange for analysis"""
        if not self.logging_enabled or not self.prompt_log_file:
            return
        
        try:
            with open(self.prompt_log_file, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*20} {stage.upper()} STAGE {'='*20}\n")
                f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Max Tokens: {max_tokens}\n")
                f.write(f"System Prompt Length: {len(system_prompt) if system_prompt else 0} chars\n")
                f.write(f"User Prompt Length: {len(user_prompt)} chars\n")
                f.write(f"Response Length: {len(response) if response else 0} chars\n")
                f.write("=" * 60 + "\n\n")
                
                if self.detailed_logging:
                    self._write_detailed_log(f, system_prompt, user_prompt, response)
                else:
                    self._write_summary_log(f, system_prompt, user_prompt, response)
                
        except Exception as e:
            print(f"⚠️ Failed to log prompt exchange: {e}")

    def _write_detailed_log(self, f, system_prompt, user_prompt, response):
        """Write detailed log with full prompts"""
        # Your existing detailed logging code here
        f.write("🔧 SYSTEM PROMPT (Instructions for the AI):\n")
        f.write("┌" + "─" * 58 + "┐\n")
        if system_prompt:
            for line in system_prompt.split('\n'):
                f.write(f"│ {line:<56} │\n")
        else:
            f.write("│ [NO SYSTEM PROMPT SPECIFIED]" + " " * 27 + "│\n")
        f.write("└" + "─" * 58 + "┘\n\n")
        
        # Log user prompt with clearer formatting
        f.write("👤 USER PROMPT (The actual question/request):\n")
        f.write("┌" + "─" * 58 + "┐\n")
        # Add line prefixes to make it clearly identifiable
        for line in user_prompt.split('\n'):
            f.write(f"│ {line:<56} │\n")
        f.write("└" + "─" * 58 + "┘\n\n")
        
        # Log combined prompt (what actually gets sent to Ollama)
        if system_prompt:
            combined_prompt = f"<|system|>\n{system_prompt}\n\n<|user|>\n{user_prompt}\n\n<|assistant|>\n"
        else:
            combined_prompt = user_prompt
        
        f.write("📤 COMBINED PROMPT (What gets sent to Ollama):\n")
        f.write("┌" + "─" * 58 + "┐\n")
        for line in combined_prompt.split('\n'):
            f.write(f"│ {line:<56} │\n")
        f.write("└" + "─" * 58 + "┘\n\n")
        
        # Log response with clearer formatting
        f.write("🤖 OLLAMA RESPONSE:\n")
        f.write("┌" + "─" * 58 + "┐\n")
        if response:
            for line in response.split('\n'):
                f.write(f"│ {line:<56} │\n")
        else:
            f.write("│ [NO RESPONSE - ERROR OCCURRED]" + " " * 25 + "│\n")
        f.write("└" + "─" * 58 + "┘\n\n")
        
        # Add analysis section
        f.write("📊 ANALYSIS NOTES:\n")
        f.write("─" * 60 + "\n")
        f.write("[ Add your observations here about prompt effectiveness ]\n")
        f.write("[ Does the response follow the system prompt? ]\n")
        f.write("[ Are there improvements needed? ]\n")
        f.write("\n" + "="*80 + "\n\n")

    def _write_summary_log(self, f, system_prompt, user_prompt, response):
        """Write summary log with key information only"""
        f.write("📋 SUMMARY LOG:\n")
        f.write("─" * 60 + "\n")
        f.write(f"System prompt: {len(system_prompt) if system_prompt else 0} chars\n")
        f.write(f"User prompt: {len(user_prompt)} chars\n")
        f.write(f"Response: {len(response) if response else 0} chars\n")
        
        # Show first 100 characters of each
        if system_prompt:
            preview = system_prompt[:100].replace('\n', ' ')
            f.write(f"System preview: {preview}{'...' if len(system_prompt) > 100 else ''}\n")
        
        preview = user_prompt[:100].replace('\n', ' ')
        f.write(f"User preview: {preview}{'...' if len(user_prompt) > 100 else ''}\n")
        
        if response:
            preview = response[:100].replace('\n', ' ')
            f.write(f"Response preview: {preview}{'...' if len(response) > 100 else ''}\n")
        
        f.write("\n" + "="*80 + "\n\n")
