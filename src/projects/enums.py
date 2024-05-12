from enum import Enum


class ProjectStage(str, Enum):
    INIT = 'INIT'
    PLAN = 'PLAN'
    EXEC = 'EXEC'
    CNTRL = 'CNTRL'
    CLOSE = 'CLOSE'
