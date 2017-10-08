import numpy as np
import cv2


class LineTracker():
	def __init__(self, window_width, window_height, margin, smooth_factor):
		self.recent_centers = []
		self.window_width = window_width
		self.window_height = window_height
		self.margin = margin
		self.smooth_factor = smooth_factor

	def find_window_centroids(self, warped):
		"""
		Using convolution to detect window center. Trying to find signal from left to right
		"""

		window_centroids = []
		window = np.ones(self.window_width) #template

		l_sum = np.sum(warped[int(3*warped.shape[0]/4):,:int(warped.shape[1]/2)], axis=0)
		l_center = np.argmax(np.convolve(window, l_sum)) - self.window_width/2
		r_sum = np.sum(warped[int(3*warped.shape[0]/4):,int(warped.shape[1]/2):], axis=0)
		r_center = np.argmax(np.convolve(window, r_sum)) - self.window_width/2 + int(warped.shape[1]/2)

		window_centroids.append((l_center, r_center))

		for level in range(1, (int)(warped.shape[0] / self.window_height)):
			image_layer = np.sum(warped[int(warped.shape[0] - (level + 1)*self.window_height) : int(warped.shape[0] - level*self.window_height),:], axis=0)
			signal = np.convolve(window, image_layer)
			offset = self.window_width/2

			l_min_index = int(max(l_center+offset-self.margin, 0))
			l_max_index = int(min(l_center+offset+self.margin, warped.shape[1]))
			l_center = np.argmax(signal[l_min_index:l_max_index]) + l_min_index-offset

			r_min_index = int(max(r_center+offset-self.margin, 0))
			r_max_index = int(min(r_center+offset+self.margin, warped.shape[1]))
			r_center = np.argmax(signal[r_min_index:r_max_index]) + r_min_index-offset

			window_centroids.append((l_center, r_center))

		self.recent_centers.append(window_centroids)

		return np.average(self.recent_centers[-self.smooth_factor:], axis=0)
