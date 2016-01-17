import comp2uv_multi
import math

def comp2uv_multi_wt(x_fit_multi,uvData):
    uv_re_im_fit_multi = comp2uv_multi.comp2uv_multi(x_fit_multi,uvData)
    uv_re_im_fit_multi_wt = uv_re_im_fit_multi
    weight_idx = 5

    uv_re_im_fit_multi_wt

    for i in range(len(uv_re_im_fit_multi_wt)):
        uv_re_im_fit_multi_wt[i][0] = uv_re_im_fit_multi[i][0] * math.sqrt(uvData[i][weight_idx-1])
        uv_re_im_fit_multi_wt[i][1] = uv_re_im_fit_multi[i][1] * math.sqrt(uvData[i][weight_idx-1])

        return uv_re_im_fit_multi_wt