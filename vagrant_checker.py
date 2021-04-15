import os
import argparse
import subprocess


class VagrantBoxes:
	def __init__(self, box, *args, **kwargs):
		self.box = box
		self.all_vagrants = subprocess.check_output("vagrant global-status", shell=True)
		self.vms = []
		self.vm_running = {}
		self.vm_names = {}

	def get_boxes(self):
		clean = str(self.all_vagrants).replace("\\n", "\n").replace("-", "")
		self.vms = clean.split("\n")
		for vm in self.vms[3:]:
			try:
				if vm.split(" ")[4] == "running":
					self.vm_running[vm.split(" ")[4]] = [
						vm.split(" ")[0],
						vm.split(" ")[5].split("/")[-1],
					]
				self.vm_names[vm.split(" ")[8].split("/")[-1]] = (vm.split(" ")[0], vm.split(" ")[8])
			except IndexError:
				pass
		return self.vms

	def start(self):
		boxes = self.get_boxes()
		try:
			print(f"Shutting down {self.vm_running['running'][0]}")
			os.system(f"vagrant suspend {self.vm_running['running'][0]}")
		except KeyError:
			pass

		print(f"Starting {self.box}")
		try:
			os.system(f"vagrant up {self.vm_names[self.box]}")
			os.chdir(self.vm_names[self.box][1])
			os.system("open -a Hyper .")
		except KeyError:
			print(f"ERROR: No Vagrant Box with name {self.box}")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description="Small Script to start an pause Vagrant Boxes"
	)
	parser.add_argument("start", help="Vagrant Box to get started")
	args = parser.parse_args()
	VagrantBoxes(args.start).start()
