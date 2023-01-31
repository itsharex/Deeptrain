import { ref } from 'vue';

export class TypingEffect {
  public operation: string
  public enableCursor: boolean
  public ref: any
  private cursor: boolean;
  private index: number;
  private asLoading: number;

  constructor(operation: string, enableCursor: boolean = false) {
      this.operation = operation;
      this.enableCursor = enableCursor;
      this.ref = ref("");
      this.cursor = true;
      this.index = 0;
      this.asLoading = 0;
  }

  protected count(): void {
    this.index += 1;
    this.cursor = !this.cursor;
    const _this: TypingEffect = this;
    if (this.index <= this.operation.length) {
      this.ref.value = this.operation.substring( 0, this.index ) + ( this.cursor ? "|" : "&nbsp;" );
      setTimeout(() => (_this.count()), Math.random() * (this.enableCursor ? 200 : 100));
    } else {
      if (this.enableCursor && this.asLoading <= 11) {
        this.ref.value = this.operation + ( this.asLoading % 2 === 1 ? "|" : "&nbsp;" );
        this.asLoading += 1;
        setTimeout(() =>(_this.count()), 800);
      } else {
        this.ref.value = this.operation;
      }
    }
  }

  public run() {
    this.count();
    return this.getRef();
  }
  public getRef(): any {
    return this.ref;
  }
}
