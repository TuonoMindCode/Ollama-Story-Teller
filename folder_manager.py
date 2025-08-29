import os
import datetime
import glob

class FolderManager:
    def __init__(self, app_folders):
        """
        Initialize with dictionary of folder names and paths
        app_folders = {
            'Multi-Scene Stories': 'multiscene/stories',
            'Laboratory Scenes': 'laboratory/scenes',
            etc.
        }
        """
        self.app_folders = app_folders

    def get_folder_size(self, folder_path):
        """Calculate total size of a folder in bytes"""
        if not os.path.exists(folder_path):
            return 0
        
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(folder_path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except (OSError, FileNotFoundError):
                        # Skip files that can't be accessed
                        continue
        except (OSError, PermissionError):
            # If we can't access the folder, return 0
            return 0
        
        return total_size

    def format_size(self, size_bytes):
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

    def count_files_in_folder(self, folder_path):
        """Count total files in a folder"""
        if not os.path.exists(folder_path):
            return 0
        
        file_count = 0
        try:
            for dirpath, dirnames, filenames in os.walk(folder_path):
                file_count += len(filenames)
        except (OSError, PermissionError):
            return 0
        
        return file_count

    def get_folder_stats(self):
        """Get statistics for all app folders"""
        stats = {}
        total_size = 0
        
        for folder_name, folder_path in self.app_folders.items():
            size = self.get_folder_size(folder_path)
            file_count = self.count_files_in_folder(folder_path)
            stats[folder_name] = {
                'size': size,
                'formatted_size': self.format_size(size),
                'file_count': file_count
            }
            total_size += size
        
        stats['total'] = {
            'size': total_size,
            'formatted_size': self.format_size(total_size)
        }
        
        return stats

    def display_folder_stats_in_menu(self, current_model, current_blueprint):
        """Display folder usage statistics in the main menu"""
        print("\n" + "="*70)
        print("Ollama Story Teller")
        print("="*70)
        
        print(f"Current Model: {current_model or 'None selected'}")
        print(f"Current Blueprint: {current_blueprint or 'None selected'}")
        
        # Display folder usage statistics
        print("\nFolder Usage:")
        print("-" * 70)
        
        stats = self.get_folder_stats()
        
        # Display each folder with aligned formatting
        for folder_name, folder_stats in stats.items():
            if folder_name == 'total':
                continue  # Skip total for now
                
            # Create aligned display
            desc_padded = folder_name.ljust(25)
            size_padded = folder_stats['formatted_size'].rjust(8)
            files_text = f"({folder_stats['file_count']} files)" if folder_stats['file_count'] != 1 else f"({folder_stats['file_count']} file)"
            
            print(f"{desc_padded} {size_padded}  {files_text}")
        
        # Display total
        print("-" * 70)
        total_size = stats['total']['formatted_size']
        print(f"{'Total App Data'.ljust(25)} {total_size.rjust(8)}")

    def show_detailed_folder_stats(self):
        """Show detailed folder statistics"""
        print("\n" + "="*80)
        print("DETAILED FOLDER STATISTICS")
        print("="*80)
        
        stats = self.get_folder_stats()
        
        for folder_name, folder_path in self.app_folders.items():
            if folder_name in stats:
                folder_stats = stats[folder_name]
                
                print(f"\n{folder_name.upper()}")
                print(f"   Path: {folder_path}")
                print(f"   Size: {folder_stats['formatted_size']}")
                print(f"   Files: {folder_stats['file_count']}")
                
                # Show if folder exists
                if os.path.exists(folder_path):
                    print(f"   Status: Exists")
                    
                    # Show recent activity (optional)
                    try:
                        # Get most recent file modification time
                        latest_time = 0
                        for root, dirs, files in os.walk(folder_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                try:
                                    mtime = os.path.getmtime(file_path)
                                    latest_time = max(latest_time, mtime)
                                except OSError:
                                    continue
                        
                        if latest_time > 0:
                            modified = datetime.datetime.fromtimestamp(latest_time)
                            print(f"   Last Activity: {modified.strftime('%Y-%m-%d %H:%M:%S')}")
                    except:
                        pass
                else:
                    print(f"   Status: Does not exist")
        
        print(f"\nTOTAL APPLICATION DATA: {stats['total']['formatted_size']}")
        print("="*80)
        input("\nPress Enter to continue...")