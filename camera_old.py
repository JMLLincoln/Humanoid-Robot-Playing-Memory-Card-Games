
def compare_images(self, A, B):
    
    err = np.sum((A.astype("float") - B.astype("float")) ** 2)
    err /= float(A.shape[0] * A.shape[1])

    print("M: %s" % err)

    ssim_none = ssim(A, B, data_range = A.max() - A.min())

    print("S: %s" % ssim_none)

    im, c1, hierarchy = cv2.findContours(A, 1, 2)
    p1 = cv2.arcLength(c1[0], True)
    
    im, c2, hierarchy = cv2.findContours(B, 1, 2)
    p2 = cv2.arcLength(c2[0], True)

    if p1 > p2:
        p = p1 - p2
    else:
        p = p2 - p1
        
    print("P: %s" % p)

    if err > 5000 or ssim_none < 0.75 or p > 20:
        return False
    else:
        return True
