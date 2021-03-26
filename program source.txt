import cv2
import numpy as np
from pathlib import Path
import os
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def read_image(image_path):
    img = cv2.imread(image_path)
    with open(image_path, 'rb') as f:
        binary = f.read()
    arr = np.asarray(bytearray(binary), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)
    return img.flatten()


def make_data_list(path):
    feature_data = list()
    label_data = list()
    p = Path(path)
    image_path_list = list(p.glob("*"))
    re_image_t = os.path.join(path, "img_1")
    re_image_f = os.path.join(path, "img_0")
    for item in image_path_list:
        item = str(item)
        if item[0:47] == re_image_t:
            label_data.append(1)
            feature_data.append(read_image(item))
        elif item[0:47] == re_image_f:
            label_data.append(0)
            feature_data.append(read_image(item))
        else:
            pass
    return np.array(feature_data), label_data


def do_pca_standard(feature_data):
    sc = StandardScaler()
    feature_data_std = sc.fit_transform(feature_data)

    pca = PCA(n_components=2)
    feature_data_pca = pca.fit_transform(feature_data_std)
    return pca.components_, feature_data_std, [sc.mean_,sc.mean_]


def matrix_mean(mean_feature_data,  pca=0, axis=-1):
    if type(pca) != int:
        mean_feature_data = np.dot(pca, mean_feature_data.transpose())
        mean_feature_data = mean_feature_data.transpose()
    if axis == -1:
        return mean_feature_data.sum()/(mean_feature_data.shape[0]*mean_feature_data.shape[1])
    elif axis == 0:
        return mean_feature_data.sum(axis=0) / mean_feature_data.shape[0]


def matrix_var(matrix_feature_data, pca, axis=-1):
    matrix_feature_data = np.dot(pca, matrix_feature_data.transpose())
    if axis == -1:
        return np.cov(matrix_feature_data)


def do_gaussian_probablity_predict(gaussian_feature_data,sc, pca, var, mean_0,mean_1,n_0,n_1):
    gaussian_feature_data = np.dot(pca, gaussian_feature_data.transpose())
    gaussian_feature_data = gaussian_feature_data.transpose()
    det = np.linalg.det(var)
    var_inverse = np.linalg.inv(var)
    x_mean_0 = gaussian_feature_data-mean_0
    x_mean_1 = gaussian_feature_data-mean_1
    result_0 = (-1/2)*np.dot(np.dot(x_mean_0.transpose(), var_inverse), x_mean_0)-(1/2)*np.log(np.linalg.det(var))+np.log(n_0)
    result_1 = (-1/2)*np.dot(np.dot(x_mean_1.transpose(), var_inverse), x_mean_1)-(1/2)*np.log(np.linalg.det(var))+np.log(n_1)
    if result_0 > result_1:
        return 0
    else:
        return 1


def do_fit(fit_feature_data,fit_label_data, pca):
    fit_feature_data = list(fit_feature_data)
    fit_1_feature_data = list()
    fit_0_feature_data = list()
    count = 0
    for i in fit_label_data:
        if i == 0:
            fit_0_feature_data.append(fit_feature_data[count])
        elif i == 1:
            fit_1_feature_data.append(fit_feature_data[count])
        count += 1
    ny_1 = len(fit_1_feature_data)
    ny_0 = len(fit_0_feature_data)
    fit_1_feature_data = np.asarray(fit_1_feature_data)
    fit_0_feature_data = np.asarray(fit_0_feature_data)
    ey_0 = matrix_var(fit_0_feature_data, pca)
    ey_1 = matrix_var(fit_1_feature_data, pca)
    ey = (1/2)*(ey_0+ey_1)
    mean_0 = matrix_mean(fit_0_feature_data, pca, axis=0)
    mean_1 = matrix_mean(fit_1_feature_data, pca, axis=0)
    return ey, ny_0, ny_1, mean_0, mean_1


def main():
    a, b = make_data_list("/Users/fujiajun/nlp/probablity/usps-image")
    pca_com, feature_data, sc = do_pca_standard(a)
    var, ny_1, ny_0, mean_0, mean_1 = do_fit(feature_data,b,pca_com)
    right = 0
    for i in range(0, 1000):
        if do_gaussian_probablity_predict(feature_data[i], sc, pca_com, var,mean_0,mean_1,ny_0,ny_1) == b[i]:
            right = right + 1
    prediction_precision = right/1000
    print("正解率")
    print(prediction_precision)


main()


