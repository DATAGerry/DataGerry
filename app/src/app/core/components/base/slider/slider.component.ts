// import { Component, Input, Output, EventEmitter, OnChanges } from '@angular/core';



// import { Component, Input, Output, EventEmitter, OnChanges } from '@angular/core';

// @Component({
//   selector: 'app-form-slider',
//   templateUrl: './slider.component.html',
//   styleUrls: ['./slider.component.scss']
// })
// export class SliderComponent implements OnChanges {
//   @Input() items: any[] = [];
//   @Input() allowNotRated = true;
//   @Input() selectedId: number | null = null;

//   /** ← NEW: enable/disable “Chosen …” line (default off) */
//   @Input() showChosenText = false;

//   public sliderOptions: Array<{ id: number | null; label: string }> = [];
//   public sliderValue = 0;

//   @Output() selectedIdChange = new EventEmitter<number | null>();

//   ngOnChanges(): void {
//     this.buildSliderOptions();
//     this.syncSliderValue();
//   }

//   private buildSliderOptions(): void {
//     this.sliderOptions = [];
//     if (this.allowNotRated) {
//       this.sliderOptions.push({ id: null, label: 'Not rated' });
//     }
//     for (const it of this.items) {
//       this.sliderOptions.push({
//         id: it.public_id,
//         label: it.name || `Item ${it.public_id}`
//       });
//     }
//   }

//   private syncSliderValue(): void {
//     const idx = this.sliderOptions.findIndex(o => o.id === this.selectedId);
//     this.sliderValue = idx >= 0 ? idx : 0;
//   }

//   onSliderChange(v: string): void {
//     const idx = +v;
//     const opt = this.sliderOptions[idx];
//     this.selectedIdChange.emit(opt ? opt.id : null);
//   }
// }


import { Component, Input, Output, EventEmitter, OnChanges, SimpleChanges } from '@angular/core';

@Component({
  selector: 'app-form-slider',
  templateUrl: './slider.component.html',
  styleUrls: ['./slider.component.scss']
})
export class SliderComponent implements OnChanges {
  @Input() items: any[] = [];
  @Input() allowNotRated = true;
  @Input() selectedId: number | null = null;
  @Input() showChosenText = false;
  @Input() primaryColor = '#4171f6'; 
  @Input() disabled = false;

  public sliderOptions: Array<{ id: number | null; label: string }> = [];
  public sliderValue = 0;
  public sliderSteps: number[] = [];

  @Output() selectedIdChange = new EventEmitter<number | null>();

  ngOnChanges(changes: SimpleChanges): void {
    this.buildSliderOptions();
    this.syncSliderValue();
    this.calculateSliderSteps();
  }

  private buildSliderOptions(): void {
    this.sliderOptions = [];
    
    if (this.allowNotRated) {
      this.sliderOptions.push({ id: null, label: 'Not rated' });
    }
    
    for (const item of this.items) {
      this.sliderOptions.push({
        id: item.public_id,
        label: item.name || `Item ${item.public_id}`
      });
    }
  }

  private syncSliderValue(): void {
    const idx = this.sliderOptions.findIndex(o => o.id === this.selectedId);
    this.sliderValue = idx >= 0 ? idx : 0;
  }

  private calculateSliderSteps(): void {
    // Create an array of step positions for tick marks
    this.sliderSteps = Array.from({ length: this.sliderOptions.length }, (_, i) => i);
  }

  onSliderChange(value: string): void {
    const idx = +value;
    const option = this.sliderOptions[idx];
    this.sliderValue = idx;
    this.selectedIdChange.emit(option ? option.id : null);
  }

  getTrackFillWidth(): string {
    // Calculate percentage width for the filled part of track
    if (this.sliderSteps.length <= 1) return '0%';
    
    const percentage = (this.sliderValue / (this.sliderSteps.length - 1)) * 100;
    return `${percentage}%`;
  }
}