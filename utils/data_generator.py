from faker import Faker
import tempfile
import os
import random
import uuid
from typing import Optional, Union


class FakerGenerator:
    def __init__(self, locale='ru_RU'):
        self.fake = Faker(locale)
    
    def text(self, variant='medium') -> str:
        variants = {
            'short': lambda: self.fake.sentence(nb_words=random.randint(3, 10)),
            'medium': lambda: self.fake.text(max_nb_chars=random.randint(50, 200)),
            'long': lambda: self.fake.text(max_nb_chars=random.randint(500, 1000)),
            'multiline': lambda: '\n'.join(self.fake.sentences(random.randint(2, 5))),
        }
        
        return variants[variant]()

    
    def pin(self, digits: int = 6) -> str:
        if digits < 4 or digits > 8:
            raise ValueError("PIN must be 4-8 digits")
        
        first = str(random.randint(1, 9))
        rest = ''.join(str(random.randint(0, 9)) for _ in range(digits - 1))
        return first + rest
    
    
    def secret_id(self) -> str:
        return str(uuid.uuid4())
     
    def temp_file(
        self, 
        extension: str = '.txt', 
        content: Optional[Union[str, bytes]] = None, 
        size_kb: Optional[int] = None
    ) -> str:
        if size_kb:
            if extension in ['.bin', '.encrypted']:
                content = bytes([random.randint(0, 255) for _ in range(size_kb * 1024)])
            else:
                content = 'X' * (size_kb * 1024)
        elif content is None:
            content = self.fake.text(max_nb_chars=1000)
        
        mode = 'wb' if isinstance(content, bytes) else 'w'
        encoding = None if isinstance(content, bytes) else 'utf-8'
        
        with tempfile.NamedTemporaryFile(
            mode=mode,
            suffix=extension,
            delete=False,
            encoding=encoding
        ) as f:
            f.write(content)
            filepath = f.name
        
        return filepath
    
    def temp_txt_file(self, size_kb: Optional[int] = None) -> str:
        return self.temp_file('.txt', size_kb=size_kb)  
    
    def file_content_for_api(self, size: int = 1024) -> bytes:
        return bytes([random.randint(0, 255) for _ in range(size)])  
    
    def cleanup_files(self, *file_paths):
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception:
                pass


generator = FakerGenerator()