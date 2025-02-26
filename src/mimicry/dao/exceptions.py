

class RepositoryError(Exception):
    pass


class ConnectionRepositoryError(RepositoryError):
    pass


class MigrationRepositoryError(RepositoryError):
    pass
