import { Injectable } from '@angular/core';
import * as Papa from 'papaparse';
import { saveAs } from 'file-saver';
import jsPDF from 'jspdf';
// @ts-ignore
import autoTable from 'jspdf-autotable';

type ExportFormat = 'csv' | 'xlsx' | 'pdf';

@Injectable({ providedIn: 'root' })
export class FileExportService {


    /**
     * Export to CSV using papaparse
     */
    exportCsv(filename: string, data: any[], columns: string[], headerMap?: Record<string, string>): void {
        const mapped = this.mapFields(data, columns);
        const renamed = this.renameHeaders(mapped, headerMap, columns);
        const csv = Papa.unparse(renamed);
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        saveAs(blob, `${filename}.csv`);
    }


    /**
     * Export to XLSX using dynamic import
     */
    exportXlsx(filename: string, data: any[], columns: string[], headerMap?: Record<string, string>): void {
        const mapped = this.mapFields(data, columns);
        const renamed = this.renameHeaders(mapped, headerMap, columns);
        import('xlsx').then((xlsx: any) => {
            const worksheet = xlsx.utils.json_to_sheet(renamed);
            const workbook = { Sheets: { data: worksheet }, SheetNames: ['data'] };
            const excelBuffer = xlsx.write(workbook, { bookType: 'xlsx', type: 'array' });
            const blob = new Blob([excelBuffer], { type: 'application/octet-stream' });
            saveAs(blob, `${filename}.xlsx`);
        });
    }


    /**
     * Export to PDF using jspdf and jspdf-autotable
     */
    exportPdf(
        filename: string,
        data: any[],
        columns: string[],
        headerMap?: Record<string, string>,
        landscape: boolean = false
    ): void {
        const orientation = landscape ? 'landscape' : 'portrait';
        const doc = new jsPDF({ orientation });

        const headers = columns.map(c => headerMap?.[c] || c);
        const body = this.mapFields(data, columns).map(row =>
            columns.map(col => row[col])
        );

        autoTable(doc, {
            head: [headers],
            body: body
        });

        doc.save(`${filename}.pdf`);
    }


    /**
     * Pick and order only specified fields
     */
    private mapFields(data: any[], columns: string[]): any[] {
        return data.map(row => {
            const mapped: any = {};
            for (const col of columns) {
                // Keep boolean values as booleans
                if (typeof row[col] === 'boolean') {
                    mapped[col] = row[col];
                } else {
                    mapped[col] = row[col] ?? '';
                }
            }
            return mapped;
        });
    }


    /**
     * Rename column headers for CSV/XLSX (optional)
     */
    private renameHeaders(data: any[], headerMap?: Record<string, string>, columns?: string[]): any[] {
        if (!headerMap) return data;
        return data.map(row => {
            const renamed: any = {};
            (columns || Object.keys(row)).forEach(key => {
                renamed[headerMap[key] || key] = row[key];
            });
            return renamed;
        });
    }
}
