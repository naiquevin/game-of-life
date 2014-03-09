(ns gol-clj.core
  (:require [gol-clj.cells :as cells])
  (:require [gol-clj.game :as game])
  (:require [clojure.java.io :as io])
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


(defn display
  "Prints state after clearing the existing output"
  [state]
  (println (str (clear-str state) (render state))))


(defn random-file
  "Selects a random .cells file from a directory"
  [dir]
  (rand-nth
   (filter #(.endsWith (.getName %) ".cells")
           (file-seq dir))))


(defn handle-arg
  [arg]
  (let [file-obj (io/file arg)]
    (cond (.isDirectory file-obj)
          (let [selected (random-file file-obj)]
            (do
              (println "Randomly selected pattern: " (.getName selected))
              (print "Press enter to start")
              (flush)
              (read-line)
              selected))

          (.endsWith arg ".cells") file-obj
          :else (str "Invalid Argument: Must be path to a .cells file "
                     "or a directory containing .cells files"))))


(defn -main
  [arg]
  ;; work around dangerous default behaviour in Clojure
  (alter-var-root #'*read-eval* (constantly false))
  (let [grid (cells/grid (handle-arg arg))]
    (game/start (:cells grid) display 200)))
