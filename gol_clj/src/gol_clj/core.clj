(ns gol-clj.core
  (:require [gol-clj.cells :as cells])
  (:require [gol-clj.game :as game])
  (:gen-class))

;; Map of cell states and how they will be printed in the terminal
(def cell-repr {:alive \# :dead \space})


(defn clear-str
  "ASCII sequences for clearing whats previously written to stdout"
  [state]
  (let [n (cells/num-rows state)
        cursor-up "\u001B[1A"
        erase-line "\u001B[2K"]
    (->> [erase-line cursor-up]
         (repeat n)
         (mapcat identity)
         (cons cursor-up)
         (apply str))))


(defn render
  "Returns the world state as string to be written to stdout"
  [state]
  ((comp (partial apply str)
         (partial interpose \newline))
   (map (comp #(apply str %)
              #(map cell-repr %))
        state)))


(defn printer
  "Prints state after clearing the existing output"
  [state]
  (println (str (clear-str state) (render state))))


(defn -main
  [& args]
  ;; work around dangerous default behaviour in Clojure
  (alter-var-root #'*read-eval* (constantly false))
  (let [grid (cells/grid (first args))]
    (game/start (:cells grid) printer 200)))

