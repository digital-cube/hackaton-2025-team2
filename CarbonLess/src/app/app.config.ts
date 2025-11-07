import { ApplicationConfig, provideBrowserGlobalErrorListeners, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideNzI18n, en_US } from 'ng-zorro-antd/i18n';
import { provideHttpClient } from '@angular/common/http';
import { provideNzIcons } from 'ng-zorro-antd/icon';
import {
  MenuOutline,
  HomeOutline,
  FormOutline,
  ApartmentOutline,
  TrophyOutline,
  BarChartOutline,
  LogoutOutline,
  CarOutline,
  BulbOutline,
  SmileOutline
} from '@ant-design/icons-angular/icons';

import { routes } from './app.routes';

const icons = [
  MenuOutline,
  HomeOutline,
  FormOutline,
  ApartmentOutline,
  TrophyOutline,
  BarChartOutline,
  LogoutOutline,
  CarOutline,
  BulbOutline,
  SmileOutline
];

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideAnimationsAsync(),
    provideHttpClient(),
    provideNzI18n(en_US),
    provideNzIcons(icons)
  ]
};
