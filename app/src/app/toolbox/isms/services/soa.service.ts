import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiCallService } from 'src/app/services/api-call.service';
import { BaseApiService } from 'src/app/core/services/base-api.service';
import { ControlMeasure } from '../models/control-measure.model';

import * as Papa from 'papaparse';
import { saveAs } from 'file-saver';
import jsPDF from 'jspdf';
// @ts-ignore
import autoTable from 'jspdf-autotable';

@Injectable({ providedIn: 'root' })
export class SoaService extends BaseApiService<ControlMeasure> {
  public servicePrefix = 'isms/reports/soa';

  constructor(protected api: ApiCallService) {
    super(api);
  }

  /**
   * Fetch the full SOA list from the backend.
   */
  getSoaList(): Observable<ControlMeasure[]> {
    return this.handleGetRequest<ControlMeasure[]>(`${this.servicePrefix}`);
  }

  /**
   * Format export data: only include selected fields in fixed order
   */
  private mapExportData(data: ControlMeasure[]): any[] {
    return data.map(item => ({
      public_id: item.public_id,
      identifier: item.identifier,
      title: item.title,
      chapter: item.chapter,
      is_applicable: item.is_applicable ? '✔' : '✖',
      reason: item.reason,
      implementation_state: item.implementation_state,
      control_measure_type: item.control_measure_type,
      source: item.source
    }));
  }

  /**
   * Export SOA list to CSV format.
   */
  exportCsv(filename: string, data: ControlMeasure[]): void {
    const exportData = this.mapExportData(data);
    const csv = Papa.unparse(exportData);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    saveAs(blob, `${filename}.csv`);
  }

  /**
   * Export SOA list to XLSX format.
   */
  exportXlsx(filename: string, data: ControlMeasure[]): void {
    const exportData = this.mapExportData(data);
    import('xlsx').then((xlsx: any) => {
      const worksheet = xlsx.utils.json_to_sheet(exportData);
      const workbook = { Sheets: { data: worksheet }, SheetNames: ['data'] };
      const excelBuffer = xlsx.write(workbook, { bookType: 'xlsx', type: 'array' });
      const blob = new Blob([excelBuffer], { type: 'application/octet-stream' });
      saveAs(blob, `${filename}.xlsx`);
    });
  }

  /**
   * Export SOA list to PDF format.
   */
  exportPdf(filename: string, data: ControlMeasure[]): void {
    const exportData = this.mapExportData(data);
    const tableData = exportData.map(item => [
      item.public_id,
      item.identifier,
      item.title,
      item.chapter,
      item.is_applicable,
      item.reason,
      item.implementation_state,
      item.control_measure_type,
      item.source
    ]);

    const doc = new jsPDF();
    autoTable(doc, {
      head: [[
        'Public ID', 'Identifier', 'Title', 'Chapter', 'Applicable',
        'Reason', 'State', 'Type', 'Source'
      ]],
      body: tableData
    });

    doc.save(`${filename}.pdf`);
  }
}
