import { Component, OnInit } from '@angular/core';
import { finalize } from 'rxjs/operators';

import { Column } from 'src/app/layout/table/table.types';
import { LoaderService } from 'src/app/core/services/loader.service';
import { ToastService } from 'src/app/layout/toast/toast.service';
import { SoaService } from '../../services/soa.service';
import { ControlMeasure } from '../../models/control-measure.model';

@Component({
  selector: 'app-soa',
  templateUrl: './soa.component.html'
})
export class SoaComponent implements OnInit {
  public controls: ControlMeasure[] = [];
  public loading = false;

  public columns: Column[] = [];
  public initialVisibleColumns: string[] = [];

  constructor(
    private readonly soaService: SoaService,
    private readonly loader: LoaderService,
    private readonly toast: ToastService
  ) {}

  ngOnInit(): void {
    this.setupColumns();
    this.loadControls();
  }

  private setupColumns(): void {
    this.columns = [
      { display: 'Identifier', name: 'identifier', data: 'identifier', sortable: false },
      { display: 'Title', name: 'title', data: 'title', sortable: false },
      { display: 'Chapter', name: 'chapter', data: 'chapter', sortable: false },
      {
        display: 'Applicable',
        name: 'is_applicable',
        data: 'is_applicable',
        sortable: false,
        type: 'boolean'
      },
      { display: 'Reason', name: 'reason', data: 'reason', sortable: false },
      { display: 'State', name: 'implementation_state', data: 'implementation_state', sortable: false },
      { display: 'Type', name: 'control_measure_type', data: 'control_measure_type', sortable: false },
      { display: 'Source', name: 'source', data: 'source', sortable: false }
    ];
    this.initialVisibleColumns = this.columns.map((c) => c.name);
  }

  private loadControls(): void {
    this.loading = true;
    this.loader.show();

    this.soaService.getSoaList()
      .pipe(finalize(() => {
        this.loading = false;
        this.loader.hide();
      }))
      .subscribe({
        next: (resp) => {
          this.controls = resp;
        },
        error: (err) => {
          this.toast.error(err?.error?.message);
        }
      });
  }

  // getRowClass = (item: ControlMeasure) => item.is_applicable === false ? 'not-applicable' : '';
}
