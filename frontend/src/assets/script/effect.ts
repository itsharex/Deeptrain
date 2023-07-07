import { ref } from "vue";
import type { Ref } from "vue";

export class Typing {
  public operation: string;
  public timeout: number;
  public enableCursor: boolean;
  public ref: Ref<string>;
  private cursor: boolean;
  private index: number;
  private asLoading: number;

  constructor(
    operation: string,
    timeout: number = 800,
    enableCursor: boolean = false
  ) {
    this.operation = operation;
    this.timeout = timeout;
    this.enableCursor = enableCursor;
    this.ref = ref("");
    this.cursor = true;
    this.index = 0;
    this.asLoading = 0;
  }

  protected count(): void {
    this.index += 1;
    this.cursor = !this.cursor;
    if (this.index <= this.operation.length) {
      this.ref.value =
        this.operation.substring(0, this.index) +
        (this.cursor ? "|" : "&nbsp;");
      this.delayerCall(Math.random() * (this.enableCursor ? 200 : 100));
    } else {
      if (this.enableCursor && this.asLoading <= 11) {
        this.ref.value =
          this.operation + (this.asLoading % 2 === 1 ? "|" : "&nbsp;");
        this.asLoading += 1;
        this.delayerCall(800);
      } else {
        this.ref.value = this.operation;
      }
    }
  }

  protected delayerCall(timeout: number): void {
    const _this = this;
    setTimeout(() => _this.count(), timeout);
  }

  public run(): Ref<string> {
    this.delayerCall(this.timeout);
    return this.ref;
  }
}
