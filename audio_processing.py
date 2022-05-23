from pickletools import pyunicode
from pydub import AudioSegment
from pydub.utils import which
import os
import traceback


class AudioProcessing():
    def __init__(self):
        # Initialize variables
        AudioSegment.converter = which("ffmpeg")
        self.clips = []
        self.clip_names = []
        self.to_append_clips = []
        self.get_audio_to_append("to_append")

        # print(os.getcwd())

        pass

    def convert(self, path, audio_clip):
        # final_clip = self.clips[0] + self.to_append_clips[0]
        self.read_audio_files(path, audio_clip)

        try:
            final_clip = AudioSegment.empty()
            clip_length = self.clips[0].duration_seconds
            
            clip__ = self.clips[0][0:((clip_length / 2) * 1000)]
            # print(clip_length / 2)

            _clip_finale = self.overlay_audio(clip__, self.to_append_clips[0][1400:])
            # clip__.append(self.to_append_clips[0], crossfade=0)
            index = 1
            start_time = 0
            while index < len(self.to_append_clips) - 1:
                start_time = start_time + (self.to_append_clips[index - 1].duration_seconds * 1000)
                _clip_finale = self.overlay_at(_clip_finale, self.to_append_clips[index][1000:], start_time)
                index = index + 1
            # _clip_finale = _clip_finale.append(self.to_append_clips[1], crossfade=0)

            final_segment = self.clips[0][((clip_length / 2) * 1000):]
            final_segment = _clip_finale.append(final_segment, crossfade=0)

            final_clip = self.overlay_at(final_segment, self.to_append_clips[len(self.to_append_clips) - 1], (clip_length - 20000))
            # final_segment.append(, crossfade=0)

            # export the clip to the output folder
            final_clip_extension = self.get_file_extension(self.clip_names[0])
            print("Extension: {}".format(final_clip_extension))
            destination_path = os.path.join("processed", self.clip_names[0])
          
            self.save(final_clip, destination_path, 'mp3')
        except Exception as e:
            raise e
        pass

    def read_audio_files(self, path, audio_clip):
        # Wrap the audio clip path with tqdm if verbose
        try:
            # Read the original audio file and the audio to join
            audio_clip_paths = os.path.join(os.path.dirname(__file__), path, audio_clip)
            # get the file extension		   		
            audio_clip_extension = self.get_file_extension(audio_clip_paths)
            print(audio_clip_extension)

            if audio_clip_extension != -1:
                # Load the audio and append it to our is
                clip = AudioSegment.from_file(audio_clip_paths, audio_clip_extension)
                self.clips.append(clip)
                self.clip_names.append(audio_clip)
                print(clip)
                pass
            else:
            # Raise an error if the file does not exist
                raise ValueError("File path error")
                pass
            
        except ValueError as e:
            return "Cannot convert an undefined audio file"

    def overlay_audio(self, first_audio, second_audio):
        try:
            second_audio = second_audio.apply_gain(+9.3)

            second_audio_length = (second_audio.duration_seconds * 1000) + 100

            audio_clip = first_audio[0: second_audio_length]
            
            audio_clip = audio_clip.overlay(second_audio)

            final_clip = audio_clip + first_audio[second_audio_length:]

            # first_audio = first_audio

            return final_clip
            pass
        except Exception as e:
            raise e

    def overlay_at(self, first_audio, second_audio, position_):
        second_audio = second_audio.apply_gain(+10)
        final = first_audio.overlay(second_audio, position=position_)

        return final

    def get_file_extension(self, filename):
        # print(filename)
        # This is a helper function to get the file extension that need to be processed
        if(os.path.isfile(filename) and os.path.getsize(filename) > 0 ):
            file_extension = os.path.splitext(filename)[1].lstrip(".")
            return file_extension
        else:
            return -1
        pass

    def save(self, final_clip, path, file_extension):
        # print(final_clip)
        final_clip.export(path, format=file_extension)
        pass

    def get_audio_to_append(self, path):
        try:
            
            append_sample_path = os.path.join(os.path.dirname(__file__), path)
            # print("File Data: "+ append_sample_path)
            for file in os.listdir(append_sample_path):
                __file = os.path.join(append_sample_path, file)
                # Check if is the file
                if os.path.isfile(__file):					
                    filename = os.fsdecode(file)
                    # Check if it end with .mp3 or any other file
                    if filename.endswith(('.mp3', '.wav', '.m4a', '.aac')):
                        extension = self.get_file_extension(__file)
                        print("File Data: "+__file)
                        append_clip = AudioSegment.from_file(__file, extension)
                        self.to_append_clips.append(append_clip)
                        # self.to_append_clips.append()
                    else:
                        continue
            print("")
            print("Finished loading audio to append!\nContinue...")

            pass
        except Exception:
            #  check 
            print(traceback.print_exc())

        pass
