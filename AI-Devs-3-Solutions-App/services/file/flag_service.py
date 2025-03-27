import os
import re
import datetime
import logging
from types import SimpleNamespace
from typing import Optional, List, Dict, Any

from .file_service import FileService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FlagService:
    """
    Service for handling flag operations.
    Uses FileService for underlying file operations.
    Maintains the existing format of flags.md file.
    """
    
    def __init__(self):
        self.file_service = FileService()
        self.flags_file = os.path.join(self.file_service.storage_dir, "flags.md")
        logger.info(f"FlagService initialized with flags_file path: {self.flags_file}")
    
    def save_flag(self, week: int, episode: int, flag: str, source: str = None) -> SimpleNamespace:
        """
        Save a flag to flags.md file in the existing format.
        
        Args:
            week: Week number
            episode: Episode number
            flag: Flag value to save (without the {{FLG:}} wrapper)
            source: Source of the flag (default is episode name)
            
        Returns:
            SimpleNamespace with success status and optional error message
        """
        try:
            logger.info(f"Attempting to save flag: week={week}, episode={episode}, flag={flag}, source={source}")
            
            # Check if flag already exists
            if self.check_flag_exists(week, episode, flag):
                logger.info(f"Flag {{{{FLG:{flag}}}}} already exists for Week {week}, Episode {episode}")
                return SimpleNamespace(
                    success=False, 
                    error=f"Flag {{{{FLG:{flag}}}}} already exists for Week {week}, Episode {episode}"
                )
            
            # Get current date and time
            now = datetime.datetime.now()
            date_str = now.strftime("%Y-%m-%d %H:%M:%S")
            
            # Determine source text
            if source is None:
                # Get episode name from episode number
                episode_names = {
                    1: "Robot Login",
                    2: "Robot Verify",
                    3: "Robot Knowledge",
                    # Add more episode names as needed
                }
                source = episode_names.get(episode, f"Episode {episode}")
            
            # Format flag entry
            flag_entry = f"- {{{{FLG:{flag}}}}} ({source}, data: {date_str})\n"
            logger.info(f"Formatted flag entry: {flag_entry}")
            
            # Check if file exists
            if not self.file_service.file_exists(self.flags_file):
                logger.info(f"Creating new flags file at: {self.flags_file}")
                # Create new file with header structure
                content = "# Znalezione flagi\n\n"
                result = self.file_service.write_file(self.flags_file, content)
                if not result.success:
                    logger.error(f"Failed to create flags file: {result.error}")
                    return result
            
            # Read existing content
            result = self.file_service.read_file(self.flags_file)
            if not result.success:
                logger.error(f"Failed to read flags file: {result.error}")
                return result
            
            content = result.content
            logger.info(f"Current content length: {len(content)}")
            
            # Check if week section exists
            week_header = f"## Week {week}"
            week_pattern = re.escape(week_header)
            week_match = re.search(week_pattern, content)
            
            # Check if episode section exists
            episode_header = f"### Episode {episode} - {source}"
            episode_pattern = re.escape(f"### Episode {episode}")
            episode_match = re.search(episode_pattern, content)
            
            if not week_match:
                logger.info(f"Week {week} section not found, adding new section")
                # Add week section at the end
                if not content.endswith("\n\n"):
                    content += "\n\n"
                content += f"{week_header}\n\n"
                
                # Add episode section
                content += f"{episode_header}\n\n"
                
                # Add flag
                content += flag_entry
            elif not episode_match:
                logger.info(f"Episode {episode} section not found, adding new section")
                # Find position after week header
                week_pos = week_match.end()
                
                # Find next week header if exists
                next_week_match = re.search(r"## Week \d+", content[week_pos:])
                if next_week_match:
                    insert_pos = week_pos + next_week_match.start()
                    # Insert episode section before next week
                    content = (
                        content[:insert_pos] + 
                        f"\n\n{episode_header}\n\n{flag_entry}\n" + 
                        content[insert_pos:]
                    )
                else:
                    # Add episode section at the end of the week
                    content += f"\n{episode_header}\n\n{flag_entry}\n"
            else:
                logger.info(f"Found existing episode section, adding flag")
                # Find position after episode header
                episode_pos = episode_match.end()
                
                # Find next episode or week header if exists
                next_header_match = re.search(r"###|##", content[episode_pos:])
                if next_header_match:
                    insert_pos = episode_pos + next_header_match.start()
                    # Insert flag before next header
                    content = (
                        content[:insert_pos] + 
                        f"{flag_entry}\n" + 
                        content[insert_pos:]
                    )
                else:
                    # Add flag at the end of the episode
                    content += f"{flag_entry}\n"
            
            # Write updated content
            logger.info(f"Writing updated content to flags file")
            result = self.file_service.write_file(self.flags_file, content)
            if not result.success:
                logger.error(f"Failed to write flags file: {result.error}")
            else:
                logger.info("Successfully saved flag")
            return result
            
        except Exception as e:
            logger.error(f"Error saving flag: {str(e)}")
            return SimpleNamespace(success=False, error=str(e))
    
    def get_flag(self, week: int, episode: int, flag_name: str = None) -> SimpleNamespace:
        """
        Get a specific flag from flags.md file.
        
        Args:
            week: Week number
            episode: Episode number
            flag_name: Optional specific flag name to find (without {{FLG:}} wrapper)
            
        Returns:
            SimpleNamespace with:
                - success: bool indicating success/failure
                - flag: str with flag value if found (or list of flags if flag_name is None)
                - error: str with error message if failed
        """
        try:
            if not self.file_service.file_exists(self.flags_file):
                return SimpleNamespace(
                    success=False, 
                    error="Flags file does not exist"
                )
                
            # Read flags file
            result = self.file_service.read_file(self.flags_file)
            if not result.success:
                return result
                
            content = result.content
            
            # Find week section
            week_pattern = rf"## Week {week}(.*?)(?=## Week \d+|$)"
            week_match = re.search(week_pattern, content, re.DOTALL)
            
            if not week_match:
                return SimpleNamespace(
                    success=False, 
                    error=f"Week {week} not found in flags file"
                )
                
            week_content = week_match.group(1)
            
            # Find episode section
            episode_pattern = rf"### Episode {episode}.*?(.*?)(?=### Episode \d+|## Week \d+|$)"
            episode_match = re.search(episode_pattern, week_content, re.DOTALL)
            
            if not episode_match:
                return SimpleNamespace(
                    success=False, 
                    error=f"Episode {episode} not found in Week {week}"
                )
                
            episode_content = episode_match.group(1)
            
            # Find flags
            flag_pattern = r"- {{FLG:(.*?)}} \((.*?), data: (.*?)\)"
            flag_matches = re.finditer(flag_pattern, episode_content)
            
            flags = []
            for match in flag_matches:
                flag_value = match.group(1)
                source = match.group(2)
                date = match.group(3)
                
                flags.append({
                    "flag": flag_value,
                    "source": source,
                    "date": date
                })
            
            if not flags:
                return SimpleNamespace(
                    success=False, 
                    error=f"No flags found for Week {week}, Episode {episode}"
                )
                
            if flag_name:
                # Find specific flag
                for flag_info in flags:
                    if flag_info["flag"] == flag_name:
                        return SimpleNamespace(success=True, flag=flag_info)
                
                return SimpleNamespace(
                    success=False, 
                    error=f"Flag {flag_name} not found for Week {week}, Episode {episode}"
                )
            else:
                # Return all flags for this episode
                return SimpleNamespace(success=True, flags=flags)
                
        except Exception as e:
            return SimpleNamespace(success=False, error=str(e))
    
    def check_flag_exists(self, week: int, episode: int, flag_name: str = None) -> bool:
        """
        Check if a flag exists for specific week and episode.
        
        Args:
            week: Week number
            episode: Episode number
            flag_name: Optional specific flag name to check (without {{FLG:}} wrapper)
            
        Returns:
            True if flag exists, False otherwise
        """
        result = self.get_flag(week, episode, flag_name)
        return result.success
    
    def get_all_flags(self) -> SimpleNamespace:
        """
        Get all flags from flags.md file.
        
        Returns:
            SimpleNamespace with:
                - success: bool indicating success/failure
                - flags: list of dicts with week, episode, and flag values if found
                - error: str with error message if failed
        """
        try:
            if not self.file_service.file_exists(self.flags_file):
                return SimpleNamespace(
                    success=True, 
                    flags=[]
                )
                
            # Read flags file
            result = self.file_service.read_file(self.flags_file)
            if not result.success:
                return result
                
            content = result.content
            
            # Find all weeks
            week_pattern = r"## Week (\d+)(.*?)(?=## Week \d+|$)"
            week_matches = re.finditer(week_pattern, content, re.DOTALL)
            
            all_flags = []
            
            for week_match in week_matches:
                week_num = int(week_match.group(1))
                week_content = week_match.group(2)
                
                # Find all episodes in this week
                episode_pattern = r"### Episode (\d+) - (.*?)(.*?)(?=### Episode \d+|## Week \d+|$)"
                episode_matches = re.finditer(episode_pattern, week_content, re.DOTALL)
                
                for episode_match in episode_matches:
                    episode_num = int(episode_match.group(1))
                    episode_name = episode_match.group(2).strip()
                    episode_content = episode_match.group(3)
                    
                    # Find all flags in this episode
                    flag_pattern = r"- {{FLG:(.*?)}} \((.*?), data: (.*?)\)"
                    flag_matches = re.finditer(flag_pattern, episode_content)
                    
                    for flag_match in flag_matches:
                        flag_value = flag_match.group(1)
                        source = flag_match.group(2)
                        date = flag_match.group(3)
                        
                        all_flags.append({
                            "week": week_num,
                            "episode": episode_num,
                            "episode_name": episode_name,
                            "flag": flag_value,
                            "source": source,
                            "date": date
                        })
            
            return SimpleNamespace(success=True, flags=all_flags)
                
        except Exception as e:
            return SimpleNamespace(success=False, error=str(e))
    
    def delete_flag(self, week: int, episode: int, flag_name: str) -> SimpleNamespace:
        """
        Delete a specific flag from flags.md file.
        
        Args:
            week: Week number
            episode: Episode number
            flag_name: Flag name to delete (without {{FLG:}} wrapper)
            
        Returns:
            SimpleNamespace with success status and optional error message
        """
        try:
            if not self.file_service.file_exists(self.flags_file):
                return SimpleNamespace(
                    success=False, 
                    error="Flags file does not exist"
                )
                
            # Read flags file
            result = self.file_service.read_file(self.flags_file)
            if not result.success:
                return result
                
            content = result.content
            
            # Find and remove the flag line
            flag_pattern = rf"- {{{{FLG:{re.escape(flag_name)}}}}} \(.*?\)\n"
            new_content = re.sub(flag_pattern, "", content)
            
            if new_content == content:
                return SimpleNamespace(
                    success=False, 
                    error=f"Flag {flag_name} not found for Week {week}, Episode {episode}"
                )
            
            # Write updated content
            return self.file_service.write_file(self.flags_file, new_content)
                
        except Exception as e:
            return SimpleNamespace(success=False, error=str(e)) 