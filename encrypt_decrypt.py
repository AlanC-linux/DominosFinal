import os
import platform

class EncryptDecrypt:
	"""
	When a game is saved, the XML representation of the game is "encrypted" to prevent cheating (i.e. manually modifying the players' hands and the board).
	The "encryption" is done by creating an ".enc" file where each character of the XML file is replaced with its hexadecimal ASCII value.
	The original file is removed.
	"""

	@staticmethod
	def file_to_string(path_to_file):
		"""
		Reads a file and returns its content as a str

		Parameters
		----------
		path_to_file: str

		Returns
		-------
		content: str
		"""
		with open(path_to_file, 'r') as f:
			content = f.read()
		return content

	@staticmethod
	def ascii_string_to_hex(input_string):
		"""
		Converts each character of an ASCII string to its 2-digit hex value and returns the string. Each character representation is separated by a space.

		Parameters
		----------
		input_string: str

		Returns
		-------
		output_string: str
		"""
		ascii_hex = [hex(ord(char))[2:] for char in input_string]
		output_string = ' '.join(ascii_hex)
		return output_string

	@staticmethod
	def encrypt_and_store_file(path_to_original_file):
		"""
		Reads the file, encrypts it and stores the encrypted version.
		It also removes the original file.

		Parameters
		----------
		path_to_original_file: str

		Returns
		-------
		None
		"""
		original_file_name, _ = os.path.splitext(path_to_original_file)
		output_string = EncryptDecrypt.ascii_string_to_hex(EncryptDecrypt.file_to_string(path_to_original_file))
		with open(original_file_name+".enc", "w+") as save_file:
			save_file.write(output_string)
		os.remove(path_to_original_file)

	@staticmethod
	def hex_to_ascii_string(input_string):
		"""
		Computes back the original string from the encrypted string.

		Parameters
		----------
		input_string: str

		Returns
		-------
		output_string: str
		"""
		list_of_hex = input_string.split(" ")
		chars = [chr(int(char, 16)) for char in list_of_hex if char != ' ']
		output_string = "".join(chars)
		return output_string

	@staticmethod
	def string_to_file(path_to_file, string_to_write):
		"""
		Writes a string to a file. Creates the file if it doesn't exist.

		Parameters
		----------
		path_to_file: str
		string_to_write: str

		Returns
		-------
		None
		"""
		with open(path_to_file, 'w+') as f:
			f.write(string_to_write)

	@staticmethod
	def decrypt_file(path_to_enc_file, target_ext):
		"""
		Decrypts the encoded file, writes back the XML file.

		Parameters
		----------
		path_to_enc_file: str
		target_ext: str ('xml' in most cases)

		Returns
		-------
		None
		"""
		encrypted_string = EncryptDecrypt.file_to_string(path_to_enc_file)
		decrypted_string = EncryptDecrypt.hex_to_ascii_string(encrypted_string)
		enc_file_name, _ = os.path.splitext(path_to_enc_file)
		with open(enc_file_name+"."+target_ext, "w+") as df:
			df.write(decrypted_string)
		#os.remove(path_to_enc_file)

if __name__ == "__main__":
	ptf = "/home/ac/Documents/Informatique/CCIE/Projet/RC/preRC2/saves/test_save.enc"
	#EncryptDecrypt.encrypt_and_store_file(ptf)
	EncryptDecrypt.decrypt_file(ptf, "xml")
