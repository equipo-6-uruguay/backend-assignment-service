Run flake8 assignments/ messaging/ assessment_service/ \
14
assignments/admin.py:5:1: E302 expected 2 blank lines, found 1
15
@admin.register(TicketAssignment)
16
^
17
assignments/application/event_publisher.py:12:1: W293 blank line contains whitespace
18
"""
19
Puerto (interface) para publicar eventos de dominio.
20
21
La implementación concreta estará en la capa de infraestructura.
22
"""
23
^
24
assignments/application/event_publisher.py:15:1: W293 blank line contains whitespace
25
26
^
27
assignments/application/event_publisher.py:20:1: W293 blank line contains whitespace
28
"""
29
Publica un evento de dominio.
30
31
Args:
32
event: Evento a publicar
33
"""
34
^
35
assignments/application/use_cases/change_assignment_priority.py:14:1: W293 blank line contains whitespace
36
"""
37
Caso de uso: Cambiar la prioridad de una asignación.
38
39
Se dispara cuando cambia la prioridad del ticket base
40
o si un supervisor cambia la prioridad directamente en la asignación.
41
"""
42
^
43
assignments/application/use_cases/change_assignment_priority.py:18:1: W293 blank line contains whitespace
44
45
^
46
assignments/application/use_cases/change_assignment_priority.py:26:1: W293 blank line contains whitespace
47
48
^
49
assignments/application/use_cases/change_assignment_priority.py:30:1: W293 blank line contains whitespace
50
"""
51
Ejecuta el cambio de prioridad de la asignación.
52
53
Args:
54
ticket_id: ID del ticket asociado
55
new_priority: Nueva prioridad a asignar
56
57
Returns:
58
Assignment modificada, o None si no existe asignación para el ticket
59
60
Raises:
61
ValueError: Si la nueva prioridad es invalida
62
"""
63
^
64
assignments/application/use_cases/change_assignment_priority.py:34:1: W293 blank line contains whitespace
65
"""
66
Ejecuta el cambio de prioridad de la asignación.
67
68
Args:
69
ticket_id: ID del ticket asociado
70
new_priority: Nueva prioridad a asignar
71
72
Returns:
73
Assignment modificada, o None si no existe asignación para el ticket
74
75
Raises:
76
ValueError: Si la nueva prioridad es invalida
77
"""
78
^
79
assignments/application/use_cases/change_assignment_priority.py:37:1: W293 blank line contains whitespace
80
"""
81
Ejecuta el cambio de prioridad de la asignación.
82
83
Args:
84
ticket_id: ID del ticket asociado
85
new_priority: Nueva prioridad a asignar
86
87
Returns:
88
Assignment modificada, o None si no existe asignación para el ticket
89
90
Raises:
91
ValueError: Si la nueva prioridad es invalida
92
"""
93
^
94
assignments/application/use_cases/change_assignment_priority.py:43:1: W293 blank line contains whitespace
95
96
^
97
assignments/application/use_cases/change_assignment_priority.py:46:1: W293 blank line contains whitespace
98
99
^
100
assignments/application/use_cases/change_assignment_priority.py:49:1: W293 blank line contains whitespace
101
102
^
103
assignments/application/use_cases/change_assignment_priority.py:52:1: W293 blank line contains whitespace
104
105
^
106
assignments/application/use_cases/create_assignment.py:18:1: W293 blank line contains whitespace
107
"""
108
Caso de uso para crear una nueva asignación de ticket.
109
110
Aplica la regla: un ticket solo puede tener una asignación activa.
111
Si ya existe, la operación es idempotente.
112
"""
113
^
114
assignments/application/use_cases/create_assignment.py:22:1: W293 blank line contains whitespace
115
116
^
117
assignments/application/use_cases/create_assignment.py:24:14: W291 trailing whitespace
118
self,
119
^
120
assignments/application/use_cases/create_assignment.py:30:1: W293 blank line contains whitespace
121
122
^
123
assignments/application/use_cases/create_assignment.py:35:1: W293 blank line contains whitespace
124
"""
125
Crea una nueva asignación.
126
Si ya existe una asignación para el ticket, la retorna sin modificar (idempotente).
127
128
Args:
129
ticket_id: ID del ticket
130
priority: Prioridad de la asignación (high, medium, low)
131
assigned_to: ID del usuario al que se asigna (opcional, referencia lógica)
132
133
Returns:
134
Assignment creada o existente
135
136
Raises:
137
ValueError: si los datos son inválidos
138
"""
139
^
140
assignments/application/use_cases/create_assignment.py:40:1: W293 blank line contains whitespace
141
"""
142
Crea una nueva asignación.
143
Si ya existe una asignación para el ticket, la retorna sin modificar (idempotente).
144
145
Args:
146
ticket_id: ID del ticket
147
priority: Prioridad de la asignación (high, medium, low)
148
assigned_to: ID del usuario al que se asigna (opcional, referencia lógica)
149
150
Returns:
151
Assignment creada o existente
152
153
Raises:
154
ValueError: si los datos son inválidos
155
"""
156
^
157
assignments/application/use_cases/create_assignment.py:43:1: W293 blank line contains whitespace
158
"""
159
Crea una nueva asignación.
160
Si ya existe una asignación para el ticket, la retorna sin modificar (idempotente).
161
162
Args:
163
ticket_id: ID del ticket
164
priority: Prioridad de la asignación (high, medium, low)
165
assigned_to: ID del usuario al que se asigna (opcional, referencia lógica)
166
167
Returns:
168
Assignment creada o existente
169
170
Raises:
171
ValueError: si los datos son inválidos
172
"""
173
^
174
assignments/application/use_cases/create_assignment.py:50:1: W293 blank line contains whitespace
175
176
^
177
assignments/application/use_cases/create_assignment.py:57:1: W293 blank line contains whitespace
178
179
^
180
assignments/application/use_cases/create_assignment.py:59:1: W293 blank line contains whitespace
181
182
^
183
assignments/application/use_cases/create_assignment.py:68:1: W293 blank line contains whitespace
184
185
^
186
assignments/application/use_cases/reassign_ticket.py:17:1: W293 blank line contains whitespace
187
"""
188
Caso de uso para reasignar un ticket (cambiar su prioridad).
189
190
Aplica la regla: solo se puede reasignar un ticket que ya tiene asignación.
191
"""
192
^
193
assignments/application/use_cases/reassign_ticket.py:20:1: W293 blank line contains whitespace
194
195
^
196
assignments/application/use_cases/reassign_ticket.py:22:14: W291 trailing whitespace
197
self,
198
^
199
assignments/application/use_cases/reassign_ticket.py:28:1: W293 blank line contains whitespace
200
201
^
202
assignments/application/use_cases/reassign_ticket.py:32:1: W293 blank line contains whitespace
203
"""
204
Reasigna un ticket cambiando su prioridad.
205
206
Args:
207
ticket_id: ID del ticket
208
new_priority: Nueva prioridad (high, medium, low)
209
210
Returns:
211
Assignment actualizada
212
213
Raises:
214
ValueError: si el ticket no tiene asignación o la prioridad es inválida
215
"""
216
^
217
assignments/application/use_cases/reassign_ticket.py:36:1: W293 blank line contains whitespace
218
"""
219
Reasigna un ticket cambiando su prioridad.
220
221
Args:
222
ticket_id: ID del ticket
223
new_priority: Nueva prioridad (high, medium, low)
224
225
Returns:
226
Assignment actualizada
227
228
Raises:
229
ValueError: si el ticket no tiene asignación o la prioridad es inválida
230
"""
231
^
232
assignments/application/use_cases/reassign_ticket.py:39:1: W293 blank line contains whitespace
233
"""
234
Reasigna un ticket cambiando su prioridad.
235
236
Args:
237
ticket_id: ID del ticket
238
new_priority: Nueva prioridad (high, medium, low)
239
240
Returns:
241
Assignment actualizada
242
243
Raises:
244
ValueError: si el ticket no tiene asignación o la prioridad es inválida
245
"""
246
^
247
assignments/application/use_cases/reassign_ticket.py:44:1: W293 blank line contains whitespace
248
249
^
250
assignments/application/use_cases/reassign_ticket.py:47:1: W293 blank line contains whitespace
251
252
^
253
assignments/application/use_cases/reassign_ticket.py:49:1: W293 blank line contains whitespace
254
255
^
256
assignments/application/use_cases/reassign_ticket.py:52:1: W293 blank line contains whitespace
257
258
^
259
assignments/application/use_cases/reassign_ticket.py:55:1: W293 blank line contains whitespace
260
261
^
262
assignments/application/use_cases/reassign_ticket.py:64:1: W293 blank line contains whitespace
263
264
^
265
assignments/application/use_cases/update_assigned_user.py:6:1: F401 'datetime.datetime' imported but unused
266
from datetime import datetime
267
^
268
assignments/application/use_cases/update_assigned_user.py:17:1: W293 blank line contains whitespace
269
"""
270
Caso de uso para actualizar el usuario asignado a un ticket.
271
272
Aplica la regla: solo se puede actualizar una asignación que ya existe.
273
"""
274
^
275
assignments/application/use_cases/update_assigned_user.py:20:1: W293 blank line contains whitespace
276
277
^
278
assignments/application/use_cases/update_assigned_user.py:22:14: W291 trailing whitespace
279
self,
280
^
281
assignments/application/use_cases/update_assigned_user.py:28:1: W293 blank line contains whitespace
282
283
^
284
assignments/application/use_cases/update_assigned_user.py:32:1: W293 blank line contains whitespace
285
"""
286
Actualiza el usuario asignado a una asignación.
287
288
Args:
289
assignment_id: ID de la asignación
290
assigned_to: ID del usuario al que se asigna (puede ser None para desasignar)
291
292
Returns:
293
Assignment actualizada
294
295
Raises:
296
ValueError: si la asignación no existe
297
"""
298
^
299
assignments/application/use_cases/update_assigned_user.py:36:1: W293 blank line contains whitespace
300
"""
301
Actualiza el usuario asignado a una asignación.
302
303
Args:
304
assignment_id: ID de la asignación
305
assigned_to: ID del usuario al que se asigna (puede ser None para desasignar)
306
307
Returns:
308
Assignment actualizada
309
310
Raises:
311
ValueError: si la asignación no existe
312
"""
313
^
314
assignments/application/use_cases/update_assigned_user.py:39:1: W293 blank line contains whitespace
315
"""
316
Actualiza el usuario asignado a una asignación.
317
318
Args:
319
assignment_id: ID de la asignación
320
assigned_to: ID del usuario al que se asigna (puede ser None para desasignar)
321
322
Returns:
323
Assignment actualizada
324
325
Raises:
326
ValueError: si la asignación no existe
327
"""
328
^
329
assignments/application/use_cases/update_assigned_user.py:44:1: W293 blank line contains whitespace
330
331
^
332
assignments/application/use_cases/update_assigned_user.py:47:1: W293 blank line contains whitespace
333
334
^
335
assignments/application/use_cases/update_assigned_user.py:51:1: W293 blank line contains whitespace
336
337
^
338
assignments/domain/entities.py:14:1: W293 blank line contains whitespace
339
"""
340
Entidad de dominio que representa una asignación de ticket.
341
342
Reglas de negocio:
343
- Cada asignación pertenece a un único ticket
344
- La prioridad debe ser válida (high, medium, low)
345
- La fecha de asignación es inmutable una vez creada
346
- assigned_to es una referencia lógica al usuario (sin foreign key)
347
"""
348
^
349
assignments/domain/entities.py:26:1: W293 blank line contains whitespace
350
351
^
352
assignments/domain/entities.py:28:1: W293 blank line contains whitespace
353
354
^
355
assignments/domain/entities.py:32:1: W293 blank line contains whitespace
356
357
^
358
assignments/domain/entities.py:37:1: W293 blank line contains whitespace
359
360
^
361
assignments/domain/entities.py:43:1: W293 blank line contains whitespace
362
363
^
364
assignments/domain/events.py:13:1: W293 blank line contains whitespace
365
366
^
367
assignments/domain/events.py:28:1: W293 blank line contains whitespace
368
369
^
370
assignments/domain/events.py:51:1: W293 blank line contains whitespace
371
372
^
373
assignments/domain/repository.py:14:1: W293 blank line contains whitespace
374
"""
375
Puerto (interface) que define las operaciones de persistencia
376
para la entidad Assignment.
377
378
El dominio depende de esta abstracción, no de la implementación concreta.
379
"""
380
^
381
assignments/domain/repository.py:17:1: W293 blank line contains whitespace
382
383
^
384
assignments/domain/repository.py:24:1: W293 blank line contains whitespace
385
"""
386
Persiste una asignación.
387
Si ya existe (tiene id), la actualiza.
388
Si no existe, la crea.
389
390
Returns:
391
Assignment con id asignado
392
"""
393
^
394
assignments/domain/repository.py:29:1: W293 blank line contains whitespace
395
396
^
397
assignments/domain/repository.py:34:1: W293 blank line contains whitespace
398
"""
399
Busca una asignación por ticket_id.
400
401
Returns:
402
Assignment si existe, None si no existe
403
"""
404
^
405
assignments/domain/repository.py:39:1: W293 blank line contains whitespace
406
407
^
408
assignments/domain/repository.py:44:1: W293 blank line contains whitespace
409
"""
410
Busca una asignación por su id.
411
412
Returns:
413
Assignment si existe, None si no existe
414
"""
415
^
416
assignments/domain/repository.py:49:1: W293 blank line contains whitespace
417
418
^
419
assignments/domain/repository.py:54:1: W293 blank line contains whitespace
420
"""
421
Retorna todas las asignaciones ordenadas por fecha (más reciente primero).
422
423
Returns:
424
Lista de Assignment
425
"""
426
^
427
assignments/domain/repository.py:59:1: W293 blank line contains whitespace
428
429
^
430
assignments/domain/repository.py:64:1: W293 blank line contains whitespace
431
"""
432
Elimina una asignación por su id.
433
434
Returns:
435
True si se eliminó, False si no existía
436
"""
437
^
438
assignments/infrastructure/django_models.py:11:1: W293 blank line contains whitespace
439
"""
440
Modelo Django que persiste la entidad Assignment.
441
442
Separado del dominio para mantener independencia del framework.
443
"""
444
^
445
assignments/infrastructure/django_models.py:24:1: W293 blank line contains whitespace
446
447
^
448
assignments/infrastructure/django_models.py:28:1: W293 blank line contains whitespace
449
450
^
451
assignments/infrastructure/messaging/event_adapter.py:15:59: W291 trailing whitespace
452
"""
453
Adaptador que traduce eventos externos (TicketCreated)
454
a operaciones del dominio Assignment.
455
456
Responsabilidad: decidir qué hacer cuando llega un evento de Ticket.
457
"""
458
459
^
460
assignments/infrastructure/messaging/event_adapter.py:17:1: W293 blank line contains whitespace
461
"""
462
Adaptador que traduce eventos externos (TicketCreated)
463
a operaciones del dominio Assignment.
464
465
Responsabilidad: decidir qué hacer cuando llega un evento de Ticket.
466
"""
467
^
468
assignments/infrastructure/messaging/event_adapter.py:20:1: W293 blank line contains whitespace
469
470
^
471
assignments/infrastructure/messaging/event_adapter.py:28:1: W293 blank line contains whitespace
472
473
^
474
assignments/infrastructure/messaging/event_adapter.py:32:1: W293 blank line contains whitespace
475
"""
476
Maneja el evento TicketCreated.
477
478
Lógica de negocio:
479
- Asigna una prioridad automáticamente al nuevo ticket
480
- La prioridad se determina de forma aleatoria (simplificado)
481
482
Args:
483
event_data: Diccionario con los datos del evento
484
"""
485
^
486
assignments/infrastructure/messaging/event_adapter.py:33:27: W291 trailing whitespace
487
"""
488
Maneja el evento TicketCreated.
489
490
Lógica de negocio:
491
- Asigna una prioridad automáticamente al nuevo ticket
492
- La prioridad se determina de forma aleatoria (simplificado)
493
494
Args:
495
event_data: Diccionario con los datos del evento
496
"""
497
498
^
499
assignments/infrastructure/messaging/event_adapter.py:36:1: W293 blank line contains whitespace
500
"""
501
Maneja el evento TicketCreated.
502
503
Lógica de negocio:
504
- Asigna una prioridad automáticamente al nuevo ticket
505
- La prioridad se determina de forma aleatoria (simplificado)
506
507
Args:
508
event_data: Diccionario con los datos del evento
509
"""
510
^
511
assignments/infrastructure/messaging/event_adapter.py:41:1: W293 blank line contains whitespace
512
513
^
514
assignments/infrastructure/messaging/event_adapter.py:45:1: W293 blank line contains whitespace
515
516
^
517
assignments/infrastructure/messaging/event_adapter.py:48:1: W293 blank line contains whitespace
518
519
^
520
assignments/infrastructure/messaging/event_adapter.py:50:1: W293 blank line contains whitespace
521
522
^
523
assignments/infrastructure/messaging/event_adapter.py:52:1: W293 blank line contains whitespace
524
525
^
526
assignments/infrastructure/messaging/event_adapter.py:62:1: W293 blank line contains whitespace
527
528
^
529
assignments/infrastructure/messaging/event_adapter.py:66:1: W293 blank line contains whitespace
530
"""
531
Maneja el evento ticket.priority_changed.
532
533
Args:
534
event_data: Diccionario con los datos del evento
535
"""
536
^
537
assignments/infrastructure/messaging/event_adapter.py:72:1: W293 blank line contains whitespace
538
539
^
540
assignments/infrastructure/messaging/event_adapter.py:76:1: W293 blank line contains whitespace
541
542
^
543
assignments/infrastructure/messaging/event_adapter.py:79:1: W293 blank line contains whitespace
544
545
^
546
assignments/infrastructure/messaging/event_adapter.py:81:1: W293 blank line contains whitespace
547
548
^
549
assignments/infrastructure/messaging/event_adapter.py:94:1: W293 blank line contains whitespace
550
551
^
552
assignments/infrastructure/messaging/event_adapter.py:98:1: W293 blank line contains whitespace
553
"""
554
Determina la prioridad de la asignación.
555
556
Extrae la prioridad del evento creado, o asigna 'unassigned' por defecto.
557
"""
558
^
559
assignments/infrastructure/messaging/event_adapter.py:105:1: W293 blank line contains whitespace
560
561
^
562
assignments/infrastructure/messaging/event_adapter.py:106:68: W291 trailing whitespace
563
# Al crearse un ticket sin prioridad, debe ser 'unassigned'
564
^
565
assignments/infrastructure/messaging/event_publisher.py:16:1: W293 blank line contains whitespace
566
"""
567
Implementación concreta del EventPublisher usando RabbitMQ.
568
569
Publica eventos de dominio a un exchange de RabbitMQ.
570
"""
571
^
572
assignments/infrastructure/messaging/event_publisher.py:19:1: W293 blank line contains whitespace
573
574
^
575
assignments/infrastructure/messaging/event_publisher.py:27:44: W291 trailing whitespace
576
'RABBITMQ_EXCHANGE_ASSIGNMENT',
577
^
578
assignments/infrastructure/messaging/event_publisher.py:30:1: W293 blank line contains whitespace
579
580
^
581
assignments/infrastructure/messaging/event_publisher.py:34:1: W293 blank line contains whitespace
582
"""
583
Publica un evento de dominio a RabbitMQ.
584
585
Args:
586
event: Evento a publicar
587
"""
588
^
589
assignments/infrastructure/messaging/event_publisher.py:43:1: W293 blank line contains whitespace
590
591
^
592
assignments/infrastructure/messaging/event_publisher.py:49:1: W293 blank line contains whitespace
593
594
^
595
assignments/infrastructure/messaging/event_publisher.py:51:1: W293 blank line contains whitespace
596
597
^
598
assignments/infrastructure/messaging/event_publisher.py:61:1: W293 blank line contains whitespace
599
600
^
601
assignments/infrastructure/messaging/event_publisher.py:63:1: W293 blank line contains whitespace
602
603
^
604
assignments/infrastructure/messaging/event_publisher.py:65:1: W293 blank line contains whitespace
605
606
^
607
assignments/infrastructure/repository.py:15:1: W293 blank line contains whitespace
608
"""
609
Implementación concreta del repositorio usando Django ORM.
610
611
Responsabilidad: traducir entre entidades de dominio y modelos Django.
612
"""
613
^
614
assignments/infrastructure/repository.py:18:1: W293 blank line contains whitespace
615
616
^
617
assignments/infrastructure/repository.py:33:1: W293 blank line contains whitespace
618
619
^
620
assignments/infrastructure/repository.py:35:1: W293 blank line contains whitespace
621
622
^
623
assignments/infrastructure/repository.py:43:1: W293 blank line contains whitespace
624
625
^
626
assignments/infrastructure/repository.py:51:1: W293 blank line contains whitespace
627
628
^
629
assignments/infrastructure/repository.py:56:1: W293 blank line contains whitespace
630
631
^
632
assignments/infrastructure/repository.py:61:1: W293 blank line contains whitespace
633
634
^
635
assignments/tasks.py:12:1: W293 blank line contains whitespace
636
"""
637
Celery task que procesa eventos de ticket en segundo plano.
638
639
Args:
640
event_data: Diccionario con los datos del evento
641
"""
642
^
643
assignments/test_integration.py:8:1: F401 'assessment_service.settings as project_settings' imported but unused
644
from assessment_service import settings as project_settings
645
^
646
assignments/tests.py:41:1: W293 blank line contains whitespace
647
648
^
649
assignments/tests.py:52:1: W293 blank line contains whitespace
650
651
^
652
assignments/tests.py:62:1: W293 blank line contains whitespace
653
654
^
655
assignments/tests.py:71:1: W293 blank line contains whitespace
656
657
^
658
assignments/tests.py:81:1: W293 blank line contains whitespace
659
660
^
661
assignments/tests.py:92:1: W293 blank line contains whitespace
662
663
^
664
assignments/tests.py:102:1: W293 blank line contains whitespace
665
666
^
667
assignments/tests.py:116:1: W293 blank line contains whitespace
668
669
^
670
assignments/tests.py:125:1: W293 blank line contains whitespace
671
672
^
673
assignments/tests.py:127:1: W293 blank line contains whitespace
674
675
^
676
assignments/tests.py:133:1: W293 blank line contains whitespace
677
678
^
679
assignments/tests.py:143:1: W293 blank line contains whitespace
680
681
^
682
assignments/tests.py:145:1: W293 blank line contains whitespace
683
684
^
685
assignments/tests.py:157:1: W293 blank line contains whitespace
686
687
^
688
assignments/tests.py:160:1: W293 blank line contains whitespace
689
690
^
691
assignments/tests.py:168:1: W293 blank line contains whitespace
692
693
^
694
assignments/tests.py:170:1: W293 blank line contains whitespace
695
696
^
697
assignments/tests.py:174:1: W293 blank line contains whitespace
698
699
^
700
assignments/tests.py:183:1: W293 blank line contains whitespace
701
702
^
703
assignments/tests.py:187:1: W293 blank line contains whitespace
704
705
^
706
assignments/tests.py:190:1: W293 blank line contains whitespace
707
708
^
709
assignments/tests.py:199:1: W293 blank line contains whitespace
710
711
^
712
assignments/tests.py:201:1: W293 blank line contains whitespace
713
714
^
715
assignments/tests.py:205:1: W293 blank line contains whitespace
716
717
^
718
assignments/tests.py:210:1: W293 blank line contains whitespace
719
720
^
721
assignments/tests.py:219:1: W293 blank line contains whitespace
722
723
^
724
assignments/tests.py:221:1: W293 blank line contains whitespace
725
726
^
727
assignments/tests.py:224:1: W293 blank line contains whitespace
728
729
^
730
assignments/tests.py:229:1: W293 blank line contains whitespace
731
732
^
733
assignments/tests.py:239:1: W293 blank line contains whitespace
734
735
^
736
assignments/tests.py:241:1: W293 blank line contains whitespace
737
738
^
739
assignments/tests.py:243:1: W293 blank line contains whitespace
740
741
^
742
assignments/tests.py:252:1: W293 blank line contains whitespace
743
744
^
745
assignments/tests.py:254:1: W293 blank line contains whitespace
746
747
^
748
assignments/tests.py:257:1: W293 blank line contains whitespace
749
750
^
751
assignments/tests.py:270:1: W293 blank line contains whitespace
752
753
^
754
assignments/tests.py:275:1: W293 blank line contains whitespace
755
756
^
757
assignments/tests.py:282:1: W293 blank line contains whitespace
758
759
^
760
assignments/tests.py:286:1: W293 blank line contains whitespace
761
762
^
763
assignments/tests.py:291:1: W293 blank line contains whitespace
764
765
^
766
assignments/tests.py:298:1: W293 blank line contains whitespace
767
768
^
769
assignments/tests.py:301:1: W293 blank line contains whitespace
770
771
^
772
assignments/tests.py:306:1: W293 blank line contains whitespace
773
774
^
775
assignments/tests.py:310:1: W293 blank line contains whitespace
776
777
^
778
assignments/tests.py:313:1: W293 blank line contains whitespace
779
780
^
781
assignments/tests.py:325:1: W293 blank line contains whitespace
782
783
^
784
assignments/tests.py:330:1: W293 blank line contains whitespace
785
786
^
787
assignments/tests.py:338:1: W293 blank line contains whitespace
788
789
^
790
assignments/tests.py:345:1: W293 blank line contains whitespace
791
792
^
793
assignments/tests.py:347:1: W293 blank line contains whitespace
794
795
^
796
assignments/tests.py:354:1: W293 blank line contains whitespace
797
798
^
799
assignments/tests.py:363:1: W293 blank line contains whitespace
800
801
^
802
assignments/tests.py:370:1: W293 blank line contains whitespace
803
804
^
805
assignments/tests.py:372:1: W293 blank line contains whitespace
806
807
^
808
assignments/tests.py:375:1: W293 blank line contains whitespace
809
810
^
811
assignments/tests.py:387:1: W293 blank line contains whitespace
812
813
^
814
assignments/tests.py:392:1: W293 blank line contains whitespace
815
816
^
817
assignments/tests.py:399:1: W293 blank line contains whitespace
818
819
^
820
assignments/tests.py:401:1: W293 blank line contains whitespace
821
822
^
823
assignments/tests.py:406:1: W293 blank line contains whitespace
824
825
^
826
assignments/tests.py:410:1: W293 blank line contains whitespace
827
828
^
829
assignments/tests.py:427:1: W293 blank line contains whitespace
830
831
^
832
assignments/tests.py:430:1: W293 blank line contains whitespace
833
834
^
835
assignments/tests.py:441:1: W293 blank line contains whitespace
836
837
^
838
assignments/tests.py:445:1: W293 blank line contains whitespace
839
840
^
841
assignments/tests.py:456:1: W293 blank line contains whitespace
842
843
^
844
assignments/tests.py:458:1: W293 blank line contains whitespace
845
846
^
847
assignments/tests.py:467:1: W293 blank line contains whitespace
848
849
^
850
assignments/tests.py:469:1: W293 blank line contains whitespace
851
852
^
853
assignments/tests.py:472:1: W293 blank line contains whitespace
854
855
^
856
assignments/tests.py:481:1: W293 blank line contains whitespace
857
858
^
859
assignments/tests.py:490:1: W293 blank line contains whitespace
860
861
^
862
assignments/tests.py:493:1: W293 blank line contains whitespace
863
864
^
865
assignments/tests.py:504:1: W293 blank line contains whitespace
866
867
^
868
assignments/tests.py:514:1: W293 blank line contains whitespace
869
870
^
871
assignments/tests.py:522:1: W293 blank line contains whitespace
872
873
^
874
assignments/tests.py:524:1: W293 blank line contains whitespace
875
876
^
877
assignments/tests.py:528:1: W293 blank line contains whitespace
878
879
^
880
assignments/tests.py:533:1: W293 blank line contains whitespace
881
882
^
883
assignments/tests.py:537:1: W293 blank line contains whitespace
884
885
^
886
assignments/tests.py:555:1: W293 blank line contains whitespace
887
888
^
889
assignments/tests.py:564:1: W293 blank line contains whitespace
890
891
^
892
assignments/tests.py:582:1: W293 blank line contains whitespace
893
894
^
895
assignments/tests.py:592:1: W293 blank line contains whitespace
896
897
^
898
assignments/tests.py:595:1: W293 blank line contains whitespace
899
900
^
901
assignments/tests.py:603:1: W293 blank line contains whitespace
902
903
^
904
assignments/tests.py:617:1: W293 blank line contains whitespace
905
906
^
907
assignments/tests.py:622:1: W293 blank line contains whitespace
908
909
^
910
assignments/tests.py:626:1: W293 blank line contains whitespace
911
912
^
913
assignments/tests.py:629:1: W293 blank line contains whitespace
914
915
^
916
assignments/tests.py:636:1: W293 blank line contains whitespace
917
918
^
919
assignments/tests.py:638:1: W293 blank line contains whitespace
920
921
^
922
assignments/tests.py:678:1: W391 blank line at end of file
923
924
^
925
assignments/views.py:21:1: W293 blank line contains whitespace
926
"""
927
ViewSet para gestionar asignaciones de tickets.
928
929
Refactorizado para:
930
- No acceder directamente al ORM en operaciones de negocio
931
- Delegar lógica de negocio a casos de uso
932
- Mantener compatibilidad con Django REST Framework
933
"""
934
^
935
assignments/views.py:29:1: W293 blank line contains whitespace
936
937
^
938
assignments/views.py:34:1: W293 blank line contains whitespace
939
940
^
941
assignments/views.py:41:1: W293 blank line contains whitespace
942
943
^
944
assignments/views.py:45:1: W293 blank line contains whitespace
945
946
^
947
assignments/views.py:47:1: W293 blank line contains whitespace
948
949
^
950
assignments/views.py:54:1: W293 blank line contains whitespace
951
952
^
953
assignments/views.py:58:1: W293 blank line contains whitespace
954
955
^
956
assignments/views.py:68:1: W293 blank line contains whitespace
957
958
^
959
assignments/views.py:73:1: W293 blank line contains whitespace
960
"""
961
Reasigna un ticket (cambia su prioridad).
962
963
Endpoint: POST /assignments/reassign/
964
Body: {"ticket_id": "...", "priority": "..."}
965
"""
966
^
967
assignments/views.py:79:1: W293 blank line contains whitespace
968
969
^
970
assignments/views.py:85:1: W293 blank line contains whitespace
971
972
^
973
assignments/views.py:87:1: W293 blank line contains whitespace
974
975
^
976
assignments/views.py:93:1: W293 blank line contains whitespace
977
978
^
979
assignments/views.py:97:1: W293 blank line contains whitespace
980
981
^
982
assignments/views.py:104:1: W293 blank line contains whitespace
983
984
^
985
assignments/views.py:109:1: W293 blank line contains whitespace
986
"""
987
Asigna o reasigna un usuario a una asignación.
988
989
Endpoint: PATCH /assignments/{id}/assign-user/
990
Body: {"assigned_to": "user_id"}
991
"""
992
^
993
assignments/views.py:114:1: W293 blank line contains whitespace
994
995
^
996
assignments/views.py:116:1: W293 blank line contains whitespace
997
998
^
999
assignments/views.py:122:1: W293 blank line contains whitespace
1000
1001
^
1002
assignments/views.py:126:1: W293 blank line contains whitespace
1003
1004
^
1005
assignments/views.py:133:1: W391 blank line at end of file
1006
1007
^
1008
messaging/consumer.py:25:1: E402 module level import not at top of file
1009
import pika
1010
^
1011
messaging/consumer.py:26:1: E402 module level import not at top of file
1012
import json
1013
^
1014
messaging/consumer.py:28:1: E402 module level import not at top of file
1015
from typing import Any
1016
^
1017
messaging/consumer.py:30:1: E402 module level import not at top of file
1018
from assignments.tasks import process_ticket_event
1019
^
1020
messaging/consumer.py:31:1: E402 module level import not at top of file
1021
import time
1022
^
1023
messaging/consumer.py:32:1: E402 module level import not at top of file
1024
import logging
1025
^
1026
messaging/consumer.py:54:1: E303 too many blank lines (3)
1027
def callback(ch, method, properties, body):
1028
^
1029
messaging/consumer.py:70:1: E303 too many blank lines (3)
1030
def _setup_dead_letter_queue(channel: Any, queue_name: str) -> dict[str, str]:
1031
^
1032
messaging/handlers.py:14:1: W293 blank line contains whitespace
1033
"""
1034
Procesa eventos de ticket usando el adaptador.
1035
1036
Args:
1037
event_data: Diccionario con los datos del evento
1038
"""
1039
^
1040
messaging/handlers.py:21:1: W293 blank line contains whitespace
1041
1042
^
1043
messaging/handlers.py:23:1: W293 blank line contains whitespace
1044
1045
^
1046
messaging/test_consumer_reconnection.py:7:1: F401 'sys' imported but unused
1047
import sys
1048
^
1049
messaging/test_consumer_reconnection.py:8:1: F401 'pytest' imported but unused
1050
import pytest
1051
^
1052
messaging/test_dead_letter_queue.py:20:1: F401 'pytest' imported but unused
1053
import pytest
1054
^
1055
messaging/test_dead_letter_queue.py:21:1: F401 'unittest.mock.ANY' imported but unused
1056
from unittest.mock import patch, MagicMock, ANY, call
1057
^
1058
messaging/test_dead_letter_queue.py:21:1: F401 'unittest.mock.call' imported but unused
1059
from unittest.mock import patch, MagicMock, ANY, call
1060
^
1061
1 E302 expected 2 blank lines, found 1
1062
2 E303 too many blank lines (3)
1063
6 E402 module level import not at top of file
1064
7 F401 'datetime.datetime' imported but unused
1065
7 W291 trailing whitespace
1066
221 W293 blank line contains whitespace
1067
2 W391 blank line at end of file
1068
246
1069
Error: Process completed with exit code 1.