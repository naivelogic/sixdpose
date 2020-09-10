def ADD_score(pt_cld, true_pose, pred_pose, diameter):
    "Evaluation metric - ADD score"
    pred_pose[0:3, 0:3][np.isnan(pred_pose[0:3, 0:3])] = 1
    pred_pose[:, 3][np.isnan(pred_pose[:, 3])] = 0
    target = pt_cld @ true_pose[0:3, 0:3] + np.array(
        [true_pose[0, 3], true_pose[1, 3], true_pose[2, 3]])
    output = pt_cld @ pred_pose[0:3, 0:3] + np.array(
        [pred_pose[0, 3], pred_pose[1, 3], pred_pose[2, 3]])
    avg_distance = (np.linalg.norm(output - target))/pt_cld.shape[0]
    threshold = diameter * 0.1
    if avg_distance <= threshold:
        return 1
    else:
        return 0

