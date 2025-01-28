import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
  })
export class LoaderService {
  private loadingCounter = 0;
  private isLoadingSubject = new BehaviorSubject<boolean>(false);
  public isLoading$: Observable<boolean> = this.isLoadingSubject.asObservable();

  show(): void {
    this.loadingCounter++;
    this.updateLoadingState();
  }

  hide(): void {
    this.loadingCounter = Math.max(0, this.loadingCounter - 1);
    this.updateLoadingState();
  }

  private updateLoadingState(): void {
    console.log('counterr', this.loadingCounter)
    this.isLoadingSubject.next(this.loadingCounter > 0);
  }
}