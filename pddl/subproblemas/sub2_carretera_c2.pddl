;; =============================================================================
;; SUB-PROBLEMA 2: CONSTRUIR CARRETERA EN C2
;; Precondición: PPF ya construido
;; Objetivo: Transportar personal y maquinaria, construir carretera, retornar
;; =============================================================================

(define (problem sub2-carretera-c2)
    (:domain rescate-mina)
    
    (:objects
        C0 C1 C2 C3 - locacion
        UP - unidad_movil
        Ingeniero1 - ingeniero
        Obrero1 Obrero2 Obrero3 Obrero4 Obrero5 
        Obrero6 Obrero7 Obrero8 Obrero9 Obrero10 - obrero
        Maq1 Maq2 Maq3 Maq4 - maquinaria
        Carretera_C2 - carretera
        PPF - puente
    )
    
    (:init
        ;; Clasificación
        (base C0)
        (zona_estacionamiento C1)
        (zona_estacionamiento C2)
        
        ;; Topología
        (adyacente C0 C1)
        (adyacente C1 C0)
        (adyacente C1 C2)
        (adyacente C2 C1)
        (adyacente C2 C3)
        (adyacente C3 C2)
        
        ;; Permisos (PPF ya operativo)
        (puede_avanzar_a C0)
        (puede_avanzar_a C1)
        (puede_avanzar_a C2)
        
        ;; PPF ya construido (precondición)
        (construido PPF)
        (operativo PPF)
        (conecta PPF C1 C2)
        
        ;; Unidad en C0
        (en UP C0)
        (espacio_disponible UP)
        (puede_transportar_carga UP)
        
        ;; Personal en C0
        (en Ingeniero1 C0)
        (disponible Ingeniero1)
        
        (en Obrero1 C0) (disponible Obrero1)
        (en Obrero2 C0) (disponible Obrero2)
        (en Obrero3 C0) (disponible Obrero3)
        (en Obrero4 C0) (disponible Obrero4)
        (en Obrero5 C0) (disponible Obrero5)
        (en Obrero6 C0) (disponible Obrero6)
        (en Obrero7 C0) (disponible Obrero7)
        (en Obrero8 C0) (disponible Obrero8)
        (en Obrero9 C0) (disponible Obrero9)
        (en Obrero10 C0) (disponible Obrero10)
        
        ;; Maquinaria en C0
        (en Maq1 C0)
        (en Maq2 C0)
        (en Maq3 C0)
        (en Maq4 C0)
        
        ;; Carretera sin construir
        (en Carretera_C2 C0)
        (not (construido Carretera_C2))
        (not (operativo Carretera_C2))
    )
    
    (:goal (and
        ;; Carretera construida
        (construido Carretera_C2)
        (operativo Carretera_C2)
        (puede_avanzar_a C3)
        
        ;; Personal de regreso en C0
        (en Ingeniero1 C0)
        (en Obrero1 C0)
        (en Obrero2 C0)
        (en Obrero3 C0)
        (en Obrero4 C0)
        (en Obrero5 C0)
        (en Obrero6 C0)
        (en Obrero7 C0)
        (en Obrero8 C0)
        (en Obrero9 C0)
        (en Obrero10 C0)
        
        ;; Maquinaria de regreso
        (en Maq1 C0)
        (en Maq2 C0)
        (en Maq3 C0)
        (en Maq4 C0)
        
        ;; Unidad de regreso
        (en UP C0)
    ))
)

