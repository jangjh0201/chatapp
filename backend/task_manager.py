from backend.robot import Robot


class TaskManager:
    def __init__(self):
        self.is_making_drink = False  # 음료 만들기 상태
        self.is_using_drawer = False  # 서랍을 사용하는 작업 중 여부 (서랍 빼기/정리)

        self.robot = Robot()  # 로봇 객체 생성

    def can_use_robot(self):
        """로봇 사용 가능 여부 확인."""
        return not (self.is_making_drink or self.is_using_drawer)

    def start_making_drink(self):
        """
        음료 만들기 작업 시작. 비동기 방식으로 로봇에게 명령 전달.
        """
        if self.can_use_robot():
            self.is_making_drink = True  # 작업 상태 설정
            result = self.robot.make_drink()  # 로봇이 음료 만들기 작업을 수행
            self.finish_making_drink()
            return result

    def finish_making_drink(self):
        """음료 만들기 작업 완료."""
        self.is_making_drink = False

    def start_emptying_drawer(self):
        """
        서랍 빼기 작업 시작. 비동기 방식으로 로봇에게 명령 전달.
        """
        if self.can_use_robot():
            self.is_using_drawer = True  # 작업 상태 설정
            result = self.robot.get_items()  # 로봇이 서랍 빼기 작업을 수행
            self.finish_using_drawer()
            return result

    def start_storing_drawer(self):
        """
        서랍 정리(넣기) 작업 시작. 비동기 방식으로 로봇에게 명령 전달.
        """
        if self.can_use_robot():
            self.is_using_drawer = True  # 작업 상태 설정
            result = self.robot.put_items()  # 로봇이 서랍 정리 작업을 수행
            self.finish_using_drawer()
            return result

    def finish_using_drawer(self):
        """서랍 사용 작업 완료."""
        self.is_using_drawer = False
