import src.utils.post_processing.SkellefteaKraft as SkellefteaKraft


layout_processor = {
    "SkellefteaKraft": {
        "group": SkellefteaKraft.grp.LayoutClass,
        "agg": SkellefteaKraft.agg.Aggregate,
        "val": SkellefteaKraft.val.Validate,
    }
}
