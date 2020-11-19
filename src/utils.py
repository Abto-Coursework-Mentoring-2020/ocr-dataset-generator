def scale_bounding_boxes(original_size, target_size, bounding_boxes):
    orig_width, orig_height = original_size
    new_width, new_height = target_size

    for (orig_x1, orig_y1), (orig_x2, orig_y2) in bounding_boxes:
        x1_ratio, y1_ratio = orig_x1 / orig_width, orig_y1 / orig_height
        x1_new, y1_new = x1_ratio * new_width, y1_ratio * new_height

        x2_ratio, y2_ratio = orig_x2 / orig_width, orig_y2 / orig_height
        x2_new, y2_new = x2_ratio * new_width, y2_ratio * new_height

        yield [(round(x1_new), round(y1_new)), (round(x2_new), round(y2_new))]