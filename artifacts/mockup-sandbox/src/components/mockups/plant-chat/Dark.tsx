import React, { useState, useRef, useEffect } from "react";
import { Check, X, Search, MoreVertical, Paperclip, Smile, Mic, FastForward } from "lucide-react";
import { cn } from "@/lib/utils";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";

// Types
type Plant = {
  id: string;
  name: string;
  species: string;
  emoji: string;
};

type MessageStatus = "pending" | "accepted" | "rejected";

type Message = {
  id: string;
  plantId: string;
  text: string;
  time: string;
  status: MessageStatus;
};

// Initial Mock Data
const PLANTS: Plant[] = [
  { id: "p1", name: "Fernanda", species: "Jiboia", emoji: "🌿" },
  { id: "p2", name: "Zezinho", species: "Cacto", emoji: "🌵" },
  { id: "p3", name: "Samira", species: "Samambaia", emoji: "🪴" },
  { id: "p4", name: "Monstrinha", species: "Costela de Adão", emoji: "🍃" },
];

const INITIAL_MESSAGES: Message[] = [
  { id: "m1", plantId: "p1", text: "Tô morrendo de sede, me rega logo! (Fernanda)", time: "10:30", status: "pending" },
  { id: "m2", plantId: "p2", text: "Pode me deixar no sol, tô adorando! ☀️", time: "11:15", status: "accepted" },
  { id: "m3", plantId: "p3", text: "Coloque a planta Fernanda na geladeira.", time: "12:00", status: "pending" },
];

const CRAZY_REQUESTS = [
  "Coloque gelo na minha terra por favor 🧊",
  "Acho que vi um pulgão, SOCORRO 🐛",
  "Muda a música, eu odeio rock 🎸",
  "Quero adubo de casca de banana hoje 🍌",
  "Traz mais sol pra cá, tá escuro ☀️",
  "Tira a Samira de perto de mim, ela tá me tocando!",
  "Me dá um banho de chuva, faz favor 🌧️",
];

export function Dark() {
  const [messages, setMessages] = useState<Message[]>(INITIAL_MESSAGES);
  const [activePlantId, setActivePlantId] = useState<string>(PLANTS[0].id);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const activePlant = PLANTS.find((p) => p.id === activePlantId)!;
  const activeMessages = messages.filter((m) => m.plantId === activePlantId);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, activePlantId]);

  const handleStatusChange = (messageId: string, status: MessageStatus) => {
    setMessages((prev) =>
      prev.map((msg) => (msg.id === messageId ? { ...msg, status } : msg))
    );
  };

  const handleNovoTurno = () => {
    const newMessages: Message[] = PLANTS.map((plant, index) => {
      const randomRequest = CRAZY_REQUESTS[Math.floor(Math.random() * CRAZY_REQUESTS.length)];
      const now = new Date();
      const timeStr = `${String(now.getHours()).padStart(2, "0")}:${String(now.getMinutes()).padStart(2, "0")}`;
      return {
        id: `m_${Date.now()}_${index}`,
        plantId: plant.id,
        text: randomRequest,
        time: timeStr,
        status: "pending",
      };
    });

    setMessages((prev) => [...prev, ...newMessages]);
  };

  const getLastMessage = (plantId: string) => {
    const plantMsgs = messages.filter((m) => m.plantId === plantId);
    return plantMsgs[plantMsgs.length - 1];
  };

  return (
    <div className="flex h-screen w-full font-sans overflow-hidden text-[#e9edef]" style={{ backgroundColor: "#0a1014" }}>
      
      {/* SIDEBAR */}
      <div className="w-[30%] min-w-[300px] border-r border-[#202c33] flex flex-col" style={{ backgroundColor: "#111b21" }}>
        {/* Header */}
        <div className="h-16 px-4 flex items-center justify-between" style={{ backgroundColor: "#202c33" }}>
          <div className="flex items-center gap-3">
            <Avatar className="h-10 w-10">
              <AvatarFallback className="bg-[#005c4b] text-[#e9edef]">👨</AvatarFallback>
            </Avatar>
            <span className="font-semibold">Meu Jardim</span>
          </div>
          <div className="flex gap-4 text-[#aebac1]">
            <Search size={20} className="cursor-pointer" />
            <MoreVertical size={20} className="cursor-pointer" />
          </div>
        </div>

        {/* Plant List */}
        <div className="flex-1 overflow-y-auto">
          {PLANTS.map((plant) => {
            const lastMsg = getLastMessage(plant.id);
            const isActive = plant.id === activePlantId;
            return (
              <div
                key={plant.id}
                onClick={() => setActivePlantId(plant.id)}
                className={cn(
                  "flex items-center gap-3 px-4 py-3 cursor-pointer hover:bg-[#202c33] transition-colors",
                  isActive && "bg-[#2a3942]"
                )}
              >
                <Avatar className="h-12 w-12 text-2xl flex items-center justify-center bg-[#1b3b36]">
                  {plant.emoji}
                </Avatar>
                <div className="flex-1 min-w-0 border-b border-[#202c33] pb-3">
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-semibold truncate">{plant.name}</span>
                    {lastMsg && <span className="text-xs text-[#8696a0]">{lastMsg.time}</span>}
                  </div>
                  <div className="text-sm text-[#8696a0] truncate">
                    {lastMsg?.status === "accepted" && <Check size={14} className="inline mr-1 text-[#53bdeb]" />}
                    {lastMsg?.text || "Sem mensagens ainda."}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* MAIN CHAT AREA */}
      <div className="flex-1 flex flex-col relative" style={{ backgroundColor: "#0b141a" }}>
        {/* Chat Background Pattern (CSS Overlay) */}
        <div 
          className="absolute inset-0 opacity-[0.03] pointer-events-none"
          style={{ 
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M54.627 0l.83.83-54.627 54.627-.83-.83zM0 54.627l54.627-54.627.83.83L.83 55.457z' fill='%23ffffff' fill-rule='evenodd'/%3E%3C/svg%3E")`
          }}
        />

        {/* Header */}
        <div className="h-16 px-4 flex items-center justify-between z-10" style={{ backgroundColor: "#202c33" }}>
          <div className="flex items-center gap-3">
            <Avatar className="h-10 w-10 text-xl flex items-center justify-center bg-[#1b3b36]">
              {activePlant.emoji}
            </Avatar>
            <div className="flex flex-col">
              <span className="font-semibold">{activePlant.name}</span>
              <span className="text-xs text-[#8696a0]">{activePlant.species}</span>
            </div>
          </div>
          <div className="flex gap-4 text-[#aebac1]">
            <Search size={20} className="cursor-pointer" />
            <MoreVertical size={20} className="cursor-pointer" />
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 z-10 flex flex-col gap-4">
          <div className="bg-[#182229] text-[#8696a0] text-xs py-1 px-3 rounded-lg self-center mb-4">
            HOJE
          </div>

          {activeMessages.map((msg) => (
            <div key={msg.id} className="self-start max-w-[70%] animate-in fade-in slide-in-from-bottom-2 duration-300">
              <div 
                className={cn(
                  "p-2 rounded-lg rounded-tl-none relative shadow-sm group",
                  msg.status === "pending" && "bg-[#202c33]",
                  msg.status === "accepted" && "bg-[#005c4b] border border-[#005c4b]",
                  msg.status === "rejected" && "bg-[#3a1a1a] border border-[#5c2a2a]"
                )}
              >
                <div className={cn("text-[15px] leading-[1.3] pb-4", msg.status === "rejected" && "line-through text-[#8696a0]")}>
                  {msg.text}
                </div>
                
                <span className="text-[11px] text-[#8696a0] absolute bottom-1 right-2 flex items-center gap-1">
                  {msg.time}
                </span>

                {/* Status Indicator inside bubble */}
                {msg.status !== "pending" && (
                  <div className={cn(
                    "absolute -bottom-6 left-0 text-xs font-semibold flex items-center gap-1 animate-in fade-in zoom-in",
                    msg.status === "accepted" ? "text-[#00a884]" : "text-[#f15c6d]"
                  )}>
                    {msg.status === "accepted" ? (
                      <><Check size={14} /> Aceito!</>
                    ) : (
                      <><X size={14} /> Recusado</>
                    )}
                  </div>
                )}
              </div>

              {/* Action Buttons */}
              {msg.status === "pending" && (
                <div className="flex gap-2 mt-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button 
                    onClick={() => handleStatusChange(msg.id, "accepted")}
                    className="flex items-center gap-1 bg-[#00a884] hover:bg-[#008f6f] text-white text-xs px-2 py-1 rounded-full shadow-sm transition-colors"
                  >
                    <Check size={12} /> Aceitar
                  </button>
                  <button 
                    onClick={() => handleStatusChange(msg.id, "rejected")}
                    className="flex items-center gap-1 bg-[#ef4444] hover:bg-[#dc2626] text-white text-xs px-2 py-1 rounded-full shadow-sm transition-colors"
                  >
                    <X size={12} /> Recusar
                  </button>
                </div>
              )}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area / Turno Button */}
        <div className="p-3 flex items-center gap-4 z-10" style={{ backgroundColor: "#202c33" }}>
          <Smile size={24} className="text-[#8696a0] cursor-pointer" />
          <Paperclip size={24} className="text-[#8696a0] cursor-pointer" />
          
          <button 
            onClick={handleNovoTurno}
            className="flex-1 bg-[#00a884] hover:bg-[#008f6f] text-white font-medium py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-colors group"
          >
            <FastForward size={18} className="group-hover:translate-x-1 transition-transform" />
            ⏩ Novo Turno (Gerar Pedidos)
          </button>
          
          <Mic size={24} className="text-[#8696a0] cursor-pointer" />
        </div>
      </div>
    </div>
  );
}
