import numpy
import paddlehub as paddle
import jieba


class Audit:
    def __init__(self, use_gpu=True):
        self.lstm = paddle.Module(name="porn_detection_lstm")
        self.gru = paddle.Module(name="porn_detection_gru")
        self.cnn = paddle.Module(name="porn_detection_cnn")
        self.use_gpu = use_gpu

    @staticmethod
    def handle(data: list) -> int:
        return numpy.average([dt.get("porn_probs", 0) for dt in data])

    @staticmethod
    def detect(results) -> bool:
        """ available: return True; return False"""
        return numpy.max(results) < 0.89 and numpy.average(results) < 0.8

    def _execute(self, text: list, batch_size: int):
        return tuple(map(
            self.handle,
            (
                self.lstm.detection(data={"text": text}, use_gpu=self.use_gpu, batch_size=batch_size),
                self.gru.detection(data={"text": text}, use_gpu=self.use_gpu, batch_size=batch_size),
                self.cnn.detection(texts=text, use_gpu=self.use_gpu, batch_size=batch_size),
            )
        ))

    def execute(self, content) -> bool:
        text = jieba.lcut(content, cut_all=True, HMM=True)
        q = self._execute(text, len(text))
        return self.detect(q)

    def strict_execute(self, content) -> bool:
        for text in jieba.lcut(content, cut_all=False, HMM=True):
            text = text.strip()
            if text:
                if not self.detect(self._execute([text], 1)):
                    return False
        return True


audit = Audit()

if __name__ == "__main__":
    while 1:
        print(audit.strict_execute(input("> ")))
