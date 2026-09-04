import type { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import {
  ArrowLeftRight,
  FileCheck2,
  FileText,
  Landmark,
  Sparkles,
} from "lucide-react";
import { AnimatePresence, motion, MotionConfig } from "motion/react";
import { useState, type ComponentType, type ReactElement } from "react";

export type StageId = "deal" | "liquidity" | "treasury" | "review" | "result";
type StageStatus = "complete" | "active" | "upcoming";

type Stage = { id: StageId; label: string; status: StageStatus };
type SnapshotCard = {
  label: string;
  value: string;
  detail: string;
  status: "neutral" | "success" | "warning" | "danger";
};

export type ExperienceData = {
  product: { title: string; subtitle: string };
  stages: Stage[];
  snapshot: SnapshotCard[];
  insight: { deal: string; company: string; afterCredit: string };
  activeStage: StageId;
};

export type ExperienceState = { active_stage: StageId; primary_action?: string };
type ComponentTools = Pick<
  FrontendRendererArgs<ExperienceState, ExperienceData>,
  "setStateValue" | "setTriggerValue"
>;

const icons: Record<StageId, ComponentType<{ size?: number; "aria-hidden"?: boolean }>> = {
  deal: FileText,
  liquidity: Landmark,
  treasury: ArrowLeftRight,
  review: Sparkles,
  result: FileCheck2,
};

export default function ExperienceShell({
  data,
  setStateValue,
  setTriggerValue,
}: ComponentTools & { data: ExperienceData }): ReactElement {
  const [activeStage, setActiveStage] = useState<StageId>(data.activeStage);

  const selectStage = (stage: StageId): void => {
    setActiveStage(stage);
    setStateValue("active_stage", stage);
  };

  return (
    <MotionConfig reducedMotion="user" transition={{ duration: 0.2 }}>
      <section className="experience" aria-labelledby="experience-title">
        <header className="hero">
          <p className="eyebrow">COMPANY-AWARE TRADE TREASURY</p>
          <h1 id="experience-title">{data.product.title}</h1>
          <p>{data.product.subtitle}</p>
        </header>

        <nav className="stages" aria-label="사전점검 단계">
          {data.stages.map((stage, index) => {
            const Icon = icons[stage.id];
            const selected = activeStage === stage.id;
            const activeIndex = data.stages.findIndex((item) => item.id === activeStage);
            const status = selected ? "active" : index < activeIndex ? "complete" : "upcoming";
            return (
              <button
                className={`stage stage--${status}`}
                type="button"
                key={stage.id}
                aria-current={selected ? "step" : undefined}
                onClick={() => selectStage(stage.id)}
              >
                <Icon size={19} aria-hidden />
                <span>{stage.label}</span>
                {selected && <motion.span className="stage-indicator" layoutId="stage-indicator" />}
              </button>
            );
          })}
        </nav>

        <AnimatePresence mode="wait">
          <motion.div
            className="snapshot-grid"
            key={activeStage}
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
          >
            {data.snapshot.map((card) => (
              <motion.article
                className={`snapshot-card snapshot-card--${card.status}`}
                key={card.label}
                whileHover={{ y: -2 }}
              >
                <span>{card.label}</span>
                <strong>{card.value}</strong>
                <small>{card.detail}</small>
              </motion.article>
            ))}
          </motion.div>
        </AnimatePresence>

        <div className="insight" aria-label="회사 유동성 핵심 비교">
          <div><span>거래만 보면</span><strong>{data.insight.deal}</strong></div>
          <div><span>회사 자금계획 포함</span><strong>{data.insight.company}</strong></div>
          <div><span>미사용 한도 적용 후</span><strong>{data.insight.afterCredit}</strong></div>
        </div>

        <button
          className="primary-action"
          type="button"
          onClick={() => setTriggerValue("primary_action", "continue")}
        >
          현재 단계 확인
        </button>
      </section>
    </MotionConfig>
  );
}
