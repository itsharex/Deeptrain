from typing import List
import numpy
# import paddlehub as paddle  # hey! replace it in production env!
# import jieba


class Audit:
    def __init__(self, use_gpu=True):
        self.lstm = paddle.Module(name="porn_detection_lstm")
        self.gru = paddle.Module(name="porn_detection_gru")
        self.cnn = paddle.Module(name="porn_detection_cnn")
        self.use_gpu = use_gpu

    def _execute(self, text: List[str], batch_size: int) -> bool:
        """
        :return: Legal: return true
                 With prohibited words: return false
        """
        responses = (
            self.lstm.detection(data={"text": text}, use_gpu=self.use_gpu, batch_size=batch_size),
            self.gru.detection(data={"text": text}, use_gpu=self.use_gpu, batch_size=batch_size),
            self.cnn.detection(texts=text, use_gpu=self.use_gpu, batch_size=batch_size),
        )
        labels, probs = zip(*[(dt["porn_detection_label"], dt["porn_probs"]) for data in responses for dt in data])
        return numpy.max(probs) < 0.95 or (numpy.sum(labels) / len(labels)) < 0.5

    def execute(self, content) -> bool:
        text = jieba.lcut(content, cut_all=True, HMM=True)
        return self._execute(text, len(text))

    def strict_execute(self, content) -> bool:
        for text in jieba.lcut(content, cut_all=False, HMM=True):
            text = text.strip()
            if text and not self._execute([text], 1):
                return False
        return True


audit = Audit  # (use_gpu=False)

if __name__ == "__main__":
    from benchmark import fps_analysis
    while 1:
        val = input("> ")
        print(
            fps_analysis(
                lambda: print(audit.strict_execute(val)),
                count=1,
            ),
        )
