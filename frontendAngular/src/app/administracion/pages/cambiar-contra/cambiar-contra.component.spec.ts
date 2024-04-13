import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CambiarContraComponent } from './cambiar-contra.component';

describe('CambiarContraComponent', () => {
  let component: CambiarContraComponent;
  let fixture: ComponentFixture<CambiarContraComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [CambiarContraComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CambiarContraComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
