class PoolEmptyError(Exception):
    """
    代理池枯竭异常
    """
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('The proxy source is exhausted...')


class ResourceDepletionError(Exception):
    """
    资源枯竭异常，如果长时间抓取不到可用的代理，则触发此异常.
    """

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('There are not more proxies in internet.')
