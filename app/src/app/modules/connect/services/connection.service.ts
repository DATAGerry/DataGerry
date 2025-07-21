// /*
// * DATAGERRY - OpenSource Enterprise CMDB
// * Copyright (C) 2025 becon GmbH
// *
// * This program is free software: you can redistribute it and/or modify
// * it under the terms of the GNU Affero General Public License as
// * published by the Free Software Foundation, either version 3 of the
// * License, or (at your option) any later version.
// *
// * This program is distributed in the hope that it will be useful,
// * but WITHOUT ANY WARRANTY; without even the implied warranty of
// * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// * GNU Affero General Public License for more details.
// *
// * You should have received a copy of the GNU Affero General Public License
// * along with this program.  If not, see <https://www.gnu.org/licenses/>.
// */
import { Injectable, isDevMode } from '@angular/core';
import { HttpBackend, HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, lastValueFrom } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({ providedIn: 'root' })
export class ConnectionService {

  private readonly devPort = 4000;
  private connectionSubject: BehaviorSubject<string | null>;
  public  readonly connection: Observable<string | null>;

  private connectionStatus = false;
  private http: HttpClient;

  /* ───── getters ───── */
  get status(): boolean            { return this.connectionStatus; }
  get currentConnection(): string | null { return this.connectionSubject.value; }

  /* ───── life-cycle ───── */
  constructor(private backend: HttpBackend) {
    this.http = new HttpClient(backend);

    const stored  = environment.cloudMode ? null : localStorage.getItem('connection');
    const initial = stored && stored !== '"null"' ? JSON.parse(stored) : null;

    this.connectionSubject = new BehaviorSubject<string | null>(initial);
    this.connection        = this.connectionSubject.asObservable();


    if (environment.cloudMode && !this.currentConnection) {
      this.setConnectionURL(environment.protocol, environment.apiUrl, environment.apiPort);
      this.validateAsync();                                   // runs in background
    }


    if (!environment.cloudMode && !this.currentConnection) {
      this.injectLocalDefault();
    }

    if (!environment.cloudMode &&  this.currentConnection) {
      this.validateAsync();
    }
  }


  /** Called from the Connect screen once the user hits “Use connection”. */
  public setConnectionURL(protocol: string, host: string, port: number): void {
    host = host.replace(/^https?:\/\//, '');                  // strip any protocol
    const href = port === 0 ? `${protocol}://${host}`
                            : `${protocol}://${host}:${port}`;

    localStorage.setItem('connection', JSON.stringify(href));
    this.connectionSubject.next(href);
    this.validateAsync();
  }

    /** Tests the current connection URL and returns the response. */
  public async testCustomURL(protocol: string, host: string, port: number) {
    const url = `${protocol}://${host}:${port}/rest/`;
    return await lastValueFrom(this.http.get<any>(url));
  }

  /** Convenience for components that just want a boolean. */
  public async testConnection(): Promise<boolean> {
    try { await this.connect(); return true; }
    catch { return false; }
  }

  /* ───── private helpers ───── */

  /** Injects a sensible default only for non-cloud builds. */
  private injectLocalDefault(): void {
    if (isDevMode()) {
      this.setConnectionURL('http', '127.0.0.1', this.devPort);
    } else {
      this.setConnectionURL(
        window.location.protocol.substring(0, window.location.protocol.length - 1),
        window.location.hostname,
        +window.location.port
      );
    }
  }

  /** Background ping; keeps the `status` flag healthy. */
  private async validateAsync(): Promise<void> {
    try {
      await this.connect();
      this.connectionStatus = true;
    } catch {
      this.connectionStatus = false;
      localStorage.removeItem('connection');
      this.connectionSubject.next(null);
    }
  }


    /** Connects to the current URL and returns the response. */
  private async connect() {
    const url = `${this.currentConnection}/rest/`;
    return await lastValueFrom(this.http.get<any>(url));
  }
}