from phonemizer import phonemize
from phonemizer.backend import EspeakBackend

backend = EspeakBackend('es-419', with_stress=True)

def rate_apply(batch, rank=None, audio_column_name="audio", text_column_name="text"):
    if isinstance(batch[audio_column_name], list):  
        speaking_rates = []
        phonemes_list = []
        for text, audio in zip(batch[text_column_name], batch[audio_column_name]):
            phonemes = phonemize(text, language='es-es', backend='espeak', with_stress=True)
            
            sample_rate = audio["sampling_rate"]
            audio_length = len(audio["array"].squeeze()) / sample_rate
            
            speaking_rate = len(phonemes) / audio_length

            speaking_rates.append(speaking_rate)
            phonemes_list.append(phonemes)
        
        batch["speaking_rate"] = speaking_rates
        batch["phonemes"] = phonemes_list
    else:
        phonemes = phonemize(batch[text_column_name], language='es-es', backend='espeak', with_stress=True)
            
        sample_rate = batch[audio_column_name]["sampling_rate"]
        audio_length = len(batch[audio_column_name]["array"].squeeze()) / sample_rate
        
        speaking_rate = len(phonemes) / audio_length
        
        batch["speaking_rate"] = speaking_rate
        batch["phonemes"] = phonemes

    return batch
