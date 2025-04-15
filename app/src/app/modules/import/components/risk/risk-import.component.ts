import { Component } from '@angular/core';
import { UntypedFormControl, UntypedFormGroup, Validators } from '@angular/forms';
import { finalize } from 'rxjs';
import { LoaderService } from 'src/app/core/services/loader.service';
import { ImportService } from '../../services/import.service';
import { ToastService } from 'src/app/layout/toast/toast.service';

@Component({
    selector: 'cmdb-risk-import',
    templateUrl: './risk-import.component.html',
})
export class ImportRiskComponent {
    public fileForm: UntypedFormGroup;
    public fileName: string = 'Choose CSV file';
    public isLoading$ = this.loaderService.isLoading$;

    constructor(
        private importService: ImportService,
        private loaderService: LoaderService,
        private toastService: ToastService
    ) {
        this.fileForm = new UntypedFormGroup({
            file: new UntypedFormControl(null, Validators.required)
        });
    }

    get file() {
        return this.fileForm.get('file');
    }

    selectFile(files: FileList): void {
        if (files.length > 0) {
            const file = files[0];
            this.file.setValue(file);
            this.fileName = file.name;
        }
    }

    importRisk(): void {
        if (this.fileForm.invalid) {
            this.toastService.error('Please select a CSV file.');
            return;
        }

        const file = this.file.value;
        this.loaderService.show();
        this.importService
            .importRiskFile(file)
            .pipe(finalize(() => this.loaderService.hide()))
            .subscribe({
                next: (response) => {
                    this.toastService.success('Threat objects imported successfully!');
                },
                error: (error) => {
                    this.toastService.error(error?.error?.message);
                }
            });
    }
}