import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiCallService } from 'src/app/services/api-call.service';
import { BaseApiService } from 'src/app/core/services/base-api.service';

@Injectable({
  providedIn: 'root'
})
export class AiAssistantService extends BaseApiService<any> {
  public servicePrefix = 'ai/type_assistant/message';

  constructor(protected api: ApiCallService) {
    super(api);
  }

  /**
   * Sends a message to the AI prompt model.
   * @param message The message content to send.
   */
  postMessage(message: string): Observable<any> {
    return this.handlePostRequest<any>(`${this.servicePrefix}`, { message });
  }
}