# coding:utf-8
import numpy as np
import pandas as pd


class Pca(object):
    def __init__(self, vector_array):
        self._vector_array = vector_array

    def get_pca(self, correlation=False, sort=True):
        data = pd.DataFrame(self._vector_array, columns=['x', 'y', 'z'])
        average_data = np.mean(data, axis=0)
        decentration_matrix = data - average_data
        H = np.dot(decentration_matrix.T, decentration_matrix)
        eigenvectors, eigenvalues, eigenvectors_T = np.linalg.svd(H)

        if sort:
            sort = eigenvalues.argsort()[::-1]  # 降序排列
            eigenvalues = eigenvalues[sort]  # 索引
            eigenvectors = eigenvectors[:, sort]

        return eigenvalues, eigenvectors
