from .default import list_view, detail_view, create_view, update_view


def includeme(config):
    """Add view to our configuration."""
    config.add_view(list_view, route_name='home')
